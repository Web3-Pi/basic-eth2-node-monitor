from app.application import Application


def main():
    app = Application.create_from_arguments()

    if app:
        try:
            app.run_forever()
        except (KeyboardInterrupt, Exception):
            print()
            print("Application: interrupted by user, shutting down")
            app.shutdown()


if __name__ == '__main__':
    main()
