#!/bin/bash

cd app
uvicorn main:app --reload --log-level debug