from osumappool import ApikeyPrompt

def main():
    try:
        f = open("mykey.apikey")
    except FileNotFoundError:
        ApikeyPrompt.prompt_apikey()

if __name__ == '__main__':
    main()