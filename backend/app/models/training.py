from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum

class TrainingStatus(str, Enum):
    idle = "idle"
    collecting = "collecting"
    training = "training"
    completed = "completed"
    failed = "failed"

class TrainingMetrics(BaseModel):
    loss: float
    accuracy: float
    perplexity: float
    learning_rate: float

class TrainingSession(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    id: Optional[str] = Field(alias="_id", default=None)
    model_name: str
    base_model: str
    status: TrainingStatus = TrainingStatus.idle
    samples_collected: int = 0
    samples_target: int = 100
    current_epoch: int = 0
    total_epochs: int = 1
    metrics: Optional[TrainingMetrics] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
