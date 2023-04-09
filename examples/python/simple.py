import sys
import urllib.request

def main():
    url = sys.argv[1]
    response = urllib.request.urlopen(url)
    content = response.read()
    print(content)

if __name__ == "__main__":
    main()