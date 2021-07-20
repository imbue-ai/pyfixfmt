if __name__ == "__main__":
    try:
        from . import main
    except ImportError:
        from __init__ import main

    main()
