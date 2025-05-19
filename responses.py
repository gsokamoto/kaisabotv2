def handle_response(message) -> str:
    p_message = message.lower()

    if ("its" in p_message or "it's" in p_message) and ("time" in p_message):
        try:
            f = open("counter.txt", "r")
            counter = int(f.readline())
        except:
            f = open("counter.txt", "a")
            f.write(str(0))
        return 'o' + str(counter)



