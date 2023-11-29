# Databricks notebook source
# Example

dbutils.widgets.text("OUTPUT_PATH", "default")
OUTPUT_PATH = dbutils.widgets.get("OUTPUT_PATH")

print(f"OUTPUT_PATH: {OUTPUT_PATH}!")