#!/bin/bash

echo "Installing playwright..."

if command -v playwright &>/dev/null; then
    playwright install --with-deps
else
    echo "Playwright is not installed. Please install Playwright."
    exit 1
fi

echo "playwright installed"