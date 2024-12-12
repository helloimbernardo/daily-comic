from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import comics
import comics.exceptions

HTTP_CODE = {
    "OK": 200,
    "BAD_REQUEST": 400,
    "NOT_FOUND": 404,
    "INTERNAL_SERVER_ERROR": 500,
}


def writeResponse(self, code, message):
    setHeaders(self, code)
    self.wfile.write(message.encode("utf-8"))
    return


def setHeaders(self, code):
    self.send_response(code)
    self.send_header("Content-type", "text/plain")
    self.end_headers()
    return


def DATE_ERROR(self):
    writeResponse(self, HTTP_CODE["BAD_REQUEST"], "Invalid date format")
    return


def INTERNAL_ERROR(self):
    writeResponse(self, HTTP_CODE["INTERNAL_SERVER_ERROR"], "Unknown error")
    return


def NOT_FOUND(self):
    writeResponse(self, HTTP_CODE["NOT_FOUND"], "Invalid endpoint")
    return


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path_components = parsed_path.path.strip("/").split("/")

        if len(path_components) < 1 or not path_components[0]:
            NOT_FOUND(self)
            return
        comicQuery = path_components[0].lower()
        print(comicQuery)

        queryComponents = parse_qs(parsed_path.query)
        print(queryComponents)

        dateText = queryComponents.get("date", [""])[0]

        # reads the date to be used, if no date is provided, the current date is used
        if dateText == "":
            date = datetime.today().strftime("%m/%d/%Y")
        else:
            try:
                date = datetime.strptime(dateText, "%m-%d-%Y").strftime("%m/%d/%Y")
            except ValueError:
                DATE_ERROR(self)
                return
            except:
                INTERNAL_ERROR(self)
                return

        try:
            comic = comics.search(comicQuery).date(date)
            writeResponse(self, HTTP_CODE["OK"], comic.image_url)
        except comics.exceptions.InvalidDateError:
            DATE_ERROR(self)
        except comics.exceptions.InvalidEndpointError:
            NOT_FOUND(self)
        except Exception as e:
            INTERNAL_ERROR(self)

        return
