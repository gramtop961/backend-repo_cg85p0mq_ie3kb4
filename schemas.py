from __future__ import annotations
"""
Database Schemas for Private Trainer App

Each Pydantic model here represents a MongoDB collection. The collection name
is the lowercase of the class name (e.g., Trainer -> "trainer").

These schemas are used for validation in the backend before writing to the DB.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
import datetime as _dt

class Trainer(BaseModel):
    name: str = Field(..., description="Trainer full name")
    email: str = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    specialties: List[str] = Field(default_factory=list, description="Areas of expertise")

class Client(BaseModel):
    trainer_id: Optional[str] = Field(None, description="Assigned trainer id")
    name: str = Field(..., description="Client full name")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    goals: Optional[str] = Field(None, description="Client goals")
    notes: Optional[str] = Field(None, description="Private notes")

class Exercise(BaseModel):
    name: str = Field(..., description="Exercise name")
    sets: int = Field(3, ge=1, le=10, description="Number of sets")
    reps: int = Field(10, ge=1, le=100, description="Number of reps per set")
    tempo: Optional[str] = Field(None, description="Tempo guidance")
    rest_seconds: Optional[int] = Field(60, ge=0, description="Rest between sets in seconds")
    notes: Optional[str] = Field(None, description="Coaching cues")

class Program(BaseModel):
    trainer_id: Optional[str] = Field(None, description="Program creator trainer id")
    client_id: Optional[str] = Field(None, description="Target client id (optional)")
    title: str = Field(..., description="Program title")
    phase: Optional[str] = Field(None, description="e.g., Hypertrophy, Strength")
    exercises: List[Exercise] = Field(default_factory=list, description="List of exercises")
    notes: Optional[str] = Field(None, description="General notes")

class Session(BaseModel):
    trainer_id: str = Field(..., description="Trainer id")
    client_id: str = Field(..., description="Client id")
    date: _dt.date = Field(..., description="Session date")
    status: str = Field("scheduled", description="scheduled | completed | cancelled")
    location: Optional[str] = Field(None, description="Gym/location")
    notes: Optional[str] = Field(None, description="Session notes")

class Progress(BaseModel):
    client_id: str = Field(..., description="Client id")
    date: _dt.date = Field(..., description="Entry date")
    weight_kg: Optional[float] = Field(None, ge=0, description="Body weight in kg")
    bodyfat_pct: Optional[float] = Field(None, ge=0, le=100, description="Body fat percentage")
    measurements: Optional[str] = Field(None, description="Circumference or other metrics")
    notes: Optional[str] = Field(None, description="Notes")
