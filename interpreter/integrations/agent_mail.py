"""
Agent Mail + Beads Multi-Agent Coordination System

This module provides:
- Agent Mail: Communication between agents (Gmail-like)
- Beads: Git-backed issue tracking for agent memory
- File Reservations: Conflict avoidance system
- Worktree Management: Parallel agent workspaces
"""

import os
import json
import asyncio
import sqlite3
import hashlib
import threading
from typing import Dict, List, Optional, Any, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import uuid


class IssueStatus(Enum):
    """Status of a Beads issue."""
    BACKLOG = "backlog"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"


class ReservationStatus(Enum):
    """Status of file reservation."""
    ACTIVE = "active"
    EXPIRED = "expired"
    RELEASED = "released"


@dataclass
class Agent:
    """Represents an agent identity."""
    id: str
    name: str
    project_key: str
    program: str
    model: str
    capabilities: List[str] = field(default_factory=list)
    registered_at: datetime = field(default_factory=datetime.utcnow)
    last_active: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Message:
    """Represents a message between agents."""
    id: str
    project_key: str
    sender: str
    recipient: str
    subject: str
    body: str
    thread_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    read: bool = False


@dataclass
class FileReservation:
    """Represents a file reservation (lease)."""
    id: str
    project_key: str
    agent_name: str
    paths: List[str]
    exclusive: bool
    status: ReservationStatus
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: datetime
    ttl_seconds: int


@dataclass
class Issue:
    """Represents a Beads issue."""
    id: str
    title: str
    description: str = ""
    status: IssueStatus = IssueStatus.BACKLOG
    priority: str = "medium"
    parent_id: Optional[str] = None
    blocking: List[str] = field(default_factory=list)
    blocked_by: List[str] = field(default_factory=list)
    assignee: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


class AgentMail:
    """
    Agent Mail - Gmail-like communication for AI agents.
    
    Provides:
    - Agent identity registration
    - Async messaging between agents
    - File reservation system
    - Conflict avoidance
    """
    
    def __init__(self, base_path: str = "./mail"):
        self.base_path = base_path
        self.agents: Dict[str, Agent] = {}
        self.messages: Dict[str, List[Message]] = {}
        self.reservations: Dict[str, FileReservation] = {}
        self.db_path = os.path.join(base_path, "mail.db")
        os.makedirs(base_path, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Agents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE,
                project_key TEXT,
                program TEXT,
                model TEXT,
                capabilities TEXT,
                registered_at TEXT,
                last_active TEXT
            )
        """)
        
        # Messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                project_key TEXT,
                sender TEXT,
                recipient TEXT,
                subject TEXT,
                body TEXT,
                thread_id TEXT,
                created_at TEXT,
                read INTEGER DEFAULT 0
            )
        """)
        
        # Reservations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservations (
                id TEXT PRIMARY KEY,
                project_key TEXT,
                agent_name TEXT,
                paths TEXT,
                exclusive INTEGER,
                status TEXT,
                created_at TEXT,
                expires_at TEXT,
                ttl_seconds INTEGER
            )
        """)
        
        conn.commit()
        conn.close()
    
    def register_agent(
        self,
        name: str,
        project_key: str,
        program: str = "claude",
        model: str = "opus",
        capabilities: Optional[List[str]] = None
    ) -> Agent:
        """Register a new agent identity."""
        agent = Agent(
            id=str(uuid.uuid4())[:12],
            name=name,
            project_key=project_key,
            program=program,
            model=model,
            capabilities=capabilities or []
        )
        
        self.agents[name] = agent
        
        # Save to DB
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO agents 
            (id, name, project_key, program, model, capabilities, registered_at, last_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            agent.id, agent.name, agent.project_key,
            agent.program, agent.model,
            json.dumps(agent.capabilities),
            agent.registered_at.isoformat(),
            agent.last_active.isoformat()
        ))
        conn.commit()
        conn.close()
        
        # Initialize inbox
        if name not in self.messages:
            self.messages[name] = []
        
        return agent
    
    def send_message(
        self,
        project_key: str,
        sender: str,
        recipient: str,
        subject: str,
        body: str,
        thread_id: Optional[str] = None
    ) -> Message:
        """Send a message to another agent."""
        message = Message(
            id=str(uuid.uuid4())[:12],
            project_key=project_key,
            sender=sender,
            recipient=recipient,
            subject=subject,
            body=body,
            thread_id=thread_id or str(uuid.uuid4())[:12],
            created_at=datetime.utcnow()
        )
        
        # Add to recipient's inbox
        if recipient not in self.messages:
            self.messages[recipient] = []
        self.messages[recipient].append(message)
        
        # Save to DB
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO messages 
            (id, project_key, sender, recipient, subject, body, thread_id, created_at, read)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            message.id, message.project_key, message.sender,
            message.recipient, message.subject, message.body,
            message.thread_id, message.created_at.isoformat(), 0
        ))
        conn.commit()
        conn.close()
        
        return message
    
    def fetch_inbox(
        self, 
        agent_name: str, 
        since_ts: Optional[datetime] = None
    ) -> List[Message]:
        """Fetch messages for an agent."""
        inbox = self.messages.get(agent_name, [])
        
        if since_ts:
            inbox = [m for m in inbox if m.created_at >= since_ts]
        
        return sorted(inbox, key=lambda m: m.created_at, reverse=True)
    
    def reserve_files(
        self,
        project_key: str,
        agent_name: str,
        paths: List[str],
        exclusive: bool = True,
        ttl_seconds: int = 3600
    ) -> FileReservation:
        """Reserve files for exclusive editing."""
        # Check for conflicts
        for res_id, res in self.reservations.items():
            if res.status == ReservationStatus.ACTIVE:
                # Check path overlap
                for path in paths:
                    if any(p.startswith(path) or path.startswith(p) for p in res.paths):
                        if res.agent_name != agent_name:
                            raise ValueError(
                                f"CONFLICT: {res.agent_name} has exclusive reservation on {res.paths}"
                            )
        
        reservation = FileReservation(
            id=str(uuid.uuid4())[:12],
            project_key=project_key,
            agent_name=agent_name,
            paths=paths,
            exclusive=exclusive,
            status=ReservationStatus.ACTIVE,
            expires_at=datetime.utcnow() + timedelta(seconds=ttl_seconds),
            ttl_seconds=ttl_seconds
        )
        
        self.reservations[reservation.id] = reservation
        
        # Save to DB
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reservations 
            (id, project_key, agent_name, paths, exclusive, status, created_at, expires_at, ttl_seconds)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            reservation.id, reservation.project_key, reservation.agent_name,
            json.dumps(reservation.paths), int(reservation.exclusive),
            reservation.status.value, reservation.created_at.isoformat(),
            reservation.expires_at.isoformat(), reservation.ttl_seconds
        ))
        conn.commit()
        conn.close()
        
        return reservation
    
    def release_reservation(self, reservation_id: str) -> bool:
        """Release a file reservation."""
        if reservation_id in self.reservations:
            self.reservations[reservation_id].status = ReservationStatus.RELEASED
            return True
        return False
    
    def get_active_reservations(self, project_key: str) -> List[FileReservation]:
        """Get all active reservations for a project."""
        now = datetime.utcnow()
        active = []
        
        for res in self.reservations.values():
            if res.project_key == project_key:
                if res.status == ReservationStatus.ACTIVE:
                    if res.expires_at > now:
                        active.append(res)
                    else:
                        res.status = ReservationStatus.EXPIRED
        
        return active


class Beads:
    """
    Beads - Git-backed issue tracking for AI agents.
    
    Provides:
    - Issue graph with dependencies
    - Hash-based conflict-free IDs
    - SQLite cache for fast queries
    - Git-backed storage
    """
    
    def __init__(self, base_path: str = ".beads"):
        self.base_path = Path(base_path)
        self.issues_db = self.base_path / "issues.jsonl"
        self.cache_db = self.base_path / "cache.db"
        self.issues: Dict[str, Issue] = {}
        
        os.makedirs(base_path, exist_ok=True)
        self._init_db()
        self._load_issues()
    
    def _init_db(self):
        """Initialize SQLite cache."""
        conn = sqlite3.connect(str(self.cache_db))
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS issues (
                id TEXT PRIMARY KEY,
                title TEXT,
                description TEXT,
                status TEXT,
                priority TEXT,
                parent_id TEXT,
                blocking TEXT,
                blocked_by TEXT,
                assignee TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def _load_issues(self):
        """Load issues from JSONL."""
        if self.issues_db.exists():
            with open(self.issues_db, 'r') as f:
                for line in f:
                    data = json.loads(line)
                    issue = Issue(
                        id=data['id'],
                        title=data['title'],
                        description=data.get('description', ''),
                        status=IssueStatus(data.get('status', 'backlog')),
                        priority=data.get('priority', 'medium'),
                        parent_id=data.get('parent_id'),
                        blocking=data.get('blocking', []),
                        blocked_by=data.get('blocked_by', []),
                        assignee=data.get('assignee'),
                        created_at=datetime.fromisoformat(data['created_at']),
                        updated_at=datetime.fromisoformat(data['updated_at'])
                    )
                    self.issues[issue.id] = issue
    
    def _save_issue(self, issue: Issue):
        """Save issue to JSONL."""
        with open(self.issues_db, 'a') as f:
            f.write(json.dumps({
                'id': issue.id,
                'title': issue.title,
                'description': issue.description,
                'status': issue.status.value,
                'priority': issue.priority,
                'parent_id': issue.parent_id,
                'blocking': issue.blocking,
                'blocked_by': issue.blocked_by,
                'assignee': issue.assignee,
                'created_at': issue.created_at.isoformat(),
                'updated_at': issue.updated_at.isoformat()
            }) + '\n')
    
    def _generate_id(self, title: str) -> str:
        """Generate hash-based ID."""
        hash_input = f"{title}{datetime.utcnow().isoformat()}"
        return f"bd-{hashlib.sha256(hash_input.encode()).hexdigest()[:6]}"
    
    def create_issue(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        parent_id: Optional[str] = None,
        blocking: Optional[List[str]] = None
    ) -> Issue:
        """Create a new issue."""
        issue = Issue(
            id=self._generate_id(title),
            title=title,
            description=description,
            priority=priority,
            parent_id=parent_id,
            blocking=blocking or []
        )
        
        # Update blocked_by for blocking issues
        for blocked_id in issue.blocking:
            if blocked_id in self.issues:
                self.issues[blocked_id].blocked_by.append(issue.id)
        
        self.issues[issue.id] = issue
        self._save_issue(issue)
        
        return issue
    
    def update_issue(
        self,
        issue_id: str,
        status: Optional[IssueStatus] = None,
        assignee: Optional[str] = None,
        priority: Optional[str] = None
    ) -> Optional[Issue]:
        """Update an issue."""
        if issue_id not in self.issues:
            return None
        
        issue = self.issues[issue_id]
        
        if status:
            issue.status = status
        if assignee:
            issue.assignee = assignee
        if priority:
            issue.priority = priority
        
        issue.updated_at = datetime.utcnow()
        
        # Save updated version (append to JSONL for Git compatibility)
        self._save_issue(issue)
        
        return issue
    
    def list_issues(
        self,
        status: Optional[IssueStatus] = None,
        assignee: Optional[str] = None,
        blocked: bool = False
    ) -> List[Issue]:
        """List issues with filters."""
        results = list(self.issues.values())
        
        if status:
            results = [i for i in results if i.status == status]
        
        if assignee:
            results = [i for i in results if i.assignee == assignee]
        
        if blocked:
            results = [i for i in results if i.status != IssueStatus.BLOCKED 
                      and i.blocked_by]
        
        return sorted(results, key=lambda i: i.created_at, reverse=True)
    
    def get_ready_issues(self) -> List[Issue]:
        """Get issues that are ready to work on."""
        ready = []
        for issue in self.issues.values():
            if issue.status == IssueStatus.READY:
                # Check if blocked
                if not issue.blocked_by:
                    ready.append(issue)
                else:
                    # Check if all blockers are done
                    all_done = all(
                        self.issues.get(bid, Issue('','')).status == IssueStatus.DONE
                        for bid in issue.blocked_by
                        if bid in self.issues
                    )
                    if all_done:
                        ready.append(issue)
        
        return ready
    
    def sync(self):
        """Sync with Git (placeholder for Git operations)."""
        # In production, this would:
        # 1. Git pull
        # 2. Reload issues
        # 3. Git add/commit/push
        pass


# Singleton instances
_agent_mail_instance = None
_beads_instance = None


def get_agent_mail(base_path: str = "./mail") -> AgentMail:
    """Get or create the global Agent Mail instance."""
    global _agent_mail_instance
    if _agent_mail_instance is None:
        _agent_mail_instance = AgentMail(base_path)
    return _agent_mail_instance


def get_beads(base_path: str = ".beads") -> Beads:
    """Get or create the global Beads instance."""
    global _beads_instance
    if _beads_instance is None:
        _beads_instance = Beads(base_path)
    return _beads_instance
