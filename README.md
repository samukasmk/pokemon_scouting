# Pokémon Scouting App Guide

## Overview
This project delivers an end-to-end Pokémon scouting workflow built with Flask, SQLAlchemy, and PokeAPI. It retrieves, sanitizes, stores, and exports Pokémon data while following security, simplicity, and DSA best practices.

## Quickstart
1. **Create a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. **Install dependencies**
   ```bash
   pip install -e .[dev]
   ```
3. **Run the web API**
   ```bash
   flask --app app:create_app run --debug
   ```