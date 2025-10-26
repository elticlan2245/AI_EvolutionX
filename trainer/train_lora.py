#!/usr/bin/env python3
"""
Train LoRA adapter
"""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model
from datasets import load_dataset
from trl import SFTTrainer
from loguru import logger
import sys

def train_lora(dataset_path: str, output_dir: str):
    """Train LoRA adapter"""
    logger.info(f"🚀 Training LoRA on {dataset_path}")
    
    # Load base model
    model_name = "meta-llama/Llama-3.1-8B-Instruct"
    logger.info(f"Loading model: {model_name}")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    # LoRA config
    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    # Load dataset
    dataset = load_dataset("json", data_files=dataset_path, split="train")
    
    # Training args
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=1,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=1e-5,
        logging_steps=10,
        save_strategy="epoch",
        fp16=True,
    )
    
    # Trainer
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        tokenizer=tokenizer,
        dataset_text_field="output",
        max_seq_length=512,
    )
    
    # Train
    logger.info("Training started...")
    trainer.train()
    
    # Save
    trainer.save_model(output_dir)
    logger.info(f"✅ LoRA adapter saved to {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python train_lora.py <dataset_path> <output_dir>")
        sys.exit(1)
    
    train_lora(sys.argv[1], sys.argv[2])
