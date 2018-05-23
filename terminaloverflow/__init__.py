name = "terminaloverflow"
import terminal_overflow_loader

def main():
    print("TERMINALOVERFLOW")
    log_dir = os.path.expanduser("terminal_overflow.log")
    logging.basicConfig(filename=log_dir,level=logging.DEBUG)
    logging.debug('Application startup')

    main_terminal = terminal_overflow_layout()