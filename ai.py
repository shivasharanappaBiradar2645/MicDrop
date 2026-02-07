from google import genai
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client()


class LineItem(BaseModel):
    name: str = Field(description="Name of the product/service from the catalog.")
    description: str = Field(description="1-sentence value prop.")
    quantity: float = Field(description="Detected quantity (default to 1).")
    unit_price: float = Field(description="The calculated price per unit based on urgency/rules.")
    total_price: float = Field(description="quantity * unit_price")
    price_tier: str = Field(description="e.g., 'Standard', 'Urgency Premium', 'Discounted'")

class ChartData(BaseModel):
    title: str = Field(description="Title for the graph, e.g. 'Competitor Comparison'.")
    labels: List[str] = Field(description="X-axis labels.")
    values: List[float] = Field(description="Y-axis values.")
    colors: List[str] = Field(description="Hex codes for bars (e.g. ['#3b82f6', '#ef4444']).")

class UniversalProposal(BaseModel):
    client_name: str = Field(description="Name of the client/company.")
    executive_summary: str = Field(description="Summary of the deal.")
    urgency_detected: int = Field(description="1-10 Scale.")
    
    line_items: List[LineItem]
    
    subtotal: float
    discount_amount: float
    discount_reason: Optional[str]
    final_total: float
    
    chart: ChartData

def call_gemi(filepath,user_context):
    myfile = client.files.upload(file=filepath)
    with open("uploads/price.txt","r") as f:
        catalog_str = f.read()
        
    prompt = f"""
    You are an AI Sales Director optimized for REVENUE MAXIMIZATION.
    
    ### INPUT DATA
    1. **Catalog & Rules:** {catalog_str}
    2. **Audio:** Listen to the client's tone, pace, and specific words.
    3. **Hidden Context:** "{user_context}"

    ### YOUR PRICING ALGORITHM (Follow Step-by-Step):

    **STEP 1: EMOTIONAL ANALYSIS**
    - **Urgency Score (1-10):** - 10 = "Server is down", "Losing money", "Deadline tomorrow".
      - 1 = "Just exploring", "Planning for next year".
    - **Price Sensitivity:** - High = Mentions "budget cuts", "expensive".
      - Low = Mentions "quality", "speed", "enterprise".

    **STEP 2: PRODUCT MATCHING & QUANTITY (CRITICAL)**
    - Match needs to Catalog items.
    - **QUANTITY RULE:** If the audio does NOT explicitly state a duration (like "5 hours" or "2 days"), you MUST set Quantity = 1. Do NOT assume a full day (8 hours).

    **STEP 3: DYNAMIC PRICING CALCULATION**
    For each item, determine `unit_price`:
    
    * **A. Base Price Check:**
        - **IF Urgency >= 8 (Desperate):** Set Price CLOSE TO `max_price`. (Reason: Speed premium).
        - **IF Urgency <= 4 (Shopping Around):** Set Price CLOSE TO `base_price`. (Reason: Win the deal).
        
    * **B. Competitor Check:**
        - If they mention a competitor price, beat it by 10% (unless it violates `min_price`).

    * **C. Context Discount (APPLY LAST):**
        - If Hidden Context says "Loyal" or "Friend" -> Deduct 15% from the final total.
        - If Hidden Context says "Angry" or "Risk" -> Deduct 20% from the final total.
        - *Note: This discount applies even if urgency is high.*

    **STEP 4: OUTPUT GENERATION**
    - Generate the JSON Proposal. 
    - Adjust `executive_summary` tone to match the Context (e.g., Apologetic if Angry, Warm if Loyal).
    """
    response = client.models.generate_content(
        model='gemini-3-flash-preview',
        contents=[prompt, myfile],
        config={
            "response_mime_type": "application/json",
            "response_schema": UniversalProposal
        })
    return UniversalProposal.model_validate_json(response.text).model_dump()
