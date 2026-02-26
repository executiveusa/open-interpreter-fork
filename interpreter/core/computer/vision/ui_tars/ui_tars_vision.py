import base64
import contextlib
import io
import os
import tempfile
from PIL import Image

# Use lazy imports for heavy dependencies
from ....utils.lazy_import import lazy_import

torch = lazy_import("torch")
transformers = lazy_import("transformers")

class UiTarsVision:
    def __init__(self, computer):
        self.computer = computer
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch and torch.cuda and torch.cuda.is_available() else "cpu"
        
    def load(self):
        """Load the UI-TARS model and tokenizer"""
        try:
            # Redirect stdout/stderr to suppress loading messages
            with contextlib.redirect_stdout(open(os.devnull, "w")), \
                 contextlib.redirect_stderr(open(os.devnull, "w")):
                
                if self.computer.debug:
                    print("Loading UI-TARS-1.5-7B model...")
                
                # Check if required dependencies are available
                if not torch or not transformers:
                    raise ImportError("Required dependencies (torch, transformers) not available")
                
                # Load model and tokenizer
                model_id = "ByteDance-Seed/UI-TARS-1.5-7B"
                self.model = transformers.AutoModelForCausalLM.from_pretrained(
                    model_id,
                    trust_remote_code=True,
                    torch_dtype=torch.bfloat16,
                    device_map="auto"
                )
                self.tokenizer = transformers.AutoTokenizer.from_pretrained(
                    model_id,
                    trust_remote_code=True
                )
                
                # Set model to evaluation mode
                if self.model:
                    self.model.eval()
                
                if self.computer.debug:
                    print("UI-TARS-1.5-7B model loaded successfully")
                    
                return True
        except Exception as e:
            print(f"Error loading UI-TARS model: {e}")
            return False
    
    def query(self, 
              query="Describe this image and identify interactive elements.",
              base_64=None,
              path=None,
              lmc=None,
              pil_image=None):
        """
        Use UI-TARS to analyze an image and identify interactive elements
        """
        # Load model if not already loaded
        if self.model is None or self.tokenizer is None:
            if not self.load():
                return "Failed to load UI-TARS model"
        
        try:
            # Process image input
            img = None
            if lmc:
                if "base64" in lmc["format"]:
                    img_data = base64.b64decode(lmc["content"])
                    img = Image.open(io.BytesIO(img_data))
                elif lmc["format"] == "path":
                    img = Image.open(lmc["content"])
            elif base_64:
                img_data = base64.b64decode(base_64)
                img = Image.open(io.BytesIO(img_data))
            elif path:
                img = Image.open(path)
            elif pil_image:
                img = pil_image
            else:
                return "No image provided"
            
            if img is None:
                return "Failed to process image"
            
            # Prepare inputs for UI-TARS
            # UI-TARS expects specific formatting for GUI tasks
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": query},
                        {"type": "image"}
                    ]
                }
            ]
            
            # Process with UI-TARS model
            if torch and hasattr(torch, 'no_grad'):
                with torch.no_grad():
                    # Check if model has chat method
                    if self.model and hasattr(self.model, 'chat'):
                        response = self.model.chat(
                            image=img,
                            msgs=messages,
                            tokenizer=self.tokenizer,
                            max_new_tokens=1024
                        )
                        return response
                    else:
                        return "UI-TARS model does not have chat method"
            else:
                return "PyTorch not available"
            
        except Exception as e:
            print(f"Error querying UI-TARS model: {e}")
            return f"Error processing image with UI-TARS: {e}"
    
    def identify_elements(self, 
                         base_64=None,
                         path=None,
                         lmc=None,
                         pil_image=None):
        """
        Specifically identify interactive elements in a GUI screenshot
        """
        query = """Analyze this GUI screenshot and identify all interactive elements.
        For each element, provide:
        1. Element type (button, input field, dropdown, link, etc.)
        2. Position coordinates (x, y, width, height)
        3. Purpose/function
        4. Text content (if any)
        5. Unique identifier for automation
        
        Format your response as a structured list."""
        
        return self.query(
            query=query,
            base_64=base_64,
            path=path,
            lmc=lmc,
            pil_image=pil_image
        )