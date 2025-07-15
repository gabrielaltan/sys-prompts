#!/bin/bash

set -e

case "${1:-render}" in
    "watch"|"-w")
        echo "Starting watch mode..."
        python render.py --watch
        ;;
    "dev"|"-d")
        echo "Starting development mode..."
        python render.py --watch --verbose
        ;;
    "clean"|"-c")
        echo "Cleaning rendered files..."
        rm -rf prompts/rendered/*.md
        echo "Cleaned!"
        ;;
    "render"|"-r"|"")
        echo "Rendering templates..."
        python render.py
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  render, -r    Render templates once (default)"
        echo "  watch, -w     Watch for changes and auto-render"
        echo "  dev, -d       Watch with verbose logging"
        echo "  clean, -c     Remove all rendered files"
        echo "  help, -h      Show this help"
        ;;
    *)
        echo "Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac 