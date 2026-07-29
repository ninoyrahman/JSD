def main():
    from dviewer import dviewer

    # Initialise the viewer with your data
    jsddv = dviewer()

    # Launch the interactive window
    jsddv.run()

if __name__ == "__main__":
    main()