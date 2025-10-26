#!/usr/bin/bash
cat backend/.env.dev frontend/animize_eat/.env.dev > .env.combined.dev
cat backend/.env.dev.example frontend/animize_eat/.env.dev.example > .env.combined.dev.example 2>/dev/null
