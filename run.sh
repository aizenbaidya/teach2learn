#!/bin/bash

npm run build
exec uvicorn main:app --reload
