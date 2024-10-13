import PyPDF2
import requests
from gentopia.tools.basetool import *
import os

class PDFReaderArgs(BaseModel):
    pdf_url: str = Field(..., description="The URL of the PDF file")

class PDFReader(BaseTool):
    name = "pdf_reader"
    description = "Downloads a PDF file from a URL, reads it, and returns its text content"

    args_schema: Optional[Type[BaseModel]] = PDFReaderArgs

    def download_pdf(self, pdf_url: str, local_filename: str) -> str:
        try:
            # Download the PDF
            with requests.get(pdf_url, stream=True) as r:
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):                                                                 f.write(chunk)
            return local_filename
        except Exception as e:
            return f"Error downloading PDF: {str(e)}"
   
    def _run(self, pdf_url: str) -> str:
        local_filename = "downloaded_pdf.pdf"
        download_status = self.download_pdf(pdf_url, local_filename)

        if "Error" in download_status:
            return download_status
       
        
        try:
            with open(local_filename, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                return text[:500] + "..."
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
        finally:
            if os.path.exists(local_filename):
                os.remove(local_filename)
    
    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
    
                                                       
