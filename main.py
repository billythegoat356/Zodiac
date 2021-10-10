from genericpath import isfile
from flask import Flask, request, send_file, redirect
from pystyle import Colorate, Colors, System, Center, Write, Anime
from webbrowser import open_new as start
from socket import gethostname, gethostbyname
from os import listdir


zodiac = """
sSSSSSs   sSSSs   d ss    d d s.     sSSs.
     s   S     S  S   ~o  S S  ~O   S
    s   S       S S     b S S   `b S
   s    S       S S     S S S sSSO S
  s     S       S S     P S S    O S
 s       S     S  S    S  S S    O  S
sSSSSSs   "sss"   P ss"   P P    P   "sss'
"""


banner = '''
                   e$$$      .c.
                 4$$$$     ^$$$$$.
                 $$$$        $$$$$.
                .$$$$         $$$$$
             z$$$$$$$$       $$$$$$b
            $$$$$$""          *$$$$$$.
            $$$$$                $$$$$r
   \        $$$*     dc    ..    '$$$$b
   4       $$$F      $F    $%     $$$$$       4
   'r     4$$$L  .e$$$$$$$$$$bc    $$$$r      $
    $.    '$$$$z$$$$$$$$$$$$$$$$$..$$$$$     z$
    $$$c   $$$$$$$$$$$$$$$$$$$$$$$$$$$$F  .d$$*
      "$$$. $$$$$$$$$$$$$$$$$$$$$$$$$$P z$$$"
         "$$b$$$$$$$$$$$$$$$$$$$$$$$$$d$$*
            "$$$$$$$$$$$$$$$$$$$$$$$$$P"
^         .d$$$$$$$$$$$$$$$$$$$$$$$$"
 "e   .e$$$$*"$$$$$$$$$$$$$$$$$$$$$$$$$$e..  e"
  *$$$$P"     ^$$$$$$$$$$$$$$$$$$$$P ""**$$$$
   *"          $$$$$$$$$$$$$$$$$$$P
             .$$"*$$$$$$$$$$$$P**$$e
            z$P   J$$$$$$$$$$$e.  "$$c     .
           d$" .$$$$$$*""""*$$$$$F  "$$. .P
    ^ % e.  $$   4$$$"          ^$$     "$$"
       "*$*     "$b           $$" ^
                  $r          $
                   ".        $
                    ^'''


app = Flask("Zodiac")


def run(host: str, port: int):
    return app.run(host, port)


def render(filename: str):
    with open(filename, mode='r', encoding='utf-8') as f:
        return f.read()

def ren(text: str, status_code: int = 200) -> tuple:
    print(f"Returned {text} | Status code: {status_code}")
    return text, status_code


@app.route('/', methods=['GET'])
def main_route():
    return render('src/index.html')


@app.route('/upload', methods=['POST'])
def upload_route():
    try:
        name = request.args['filename']
        if not name.strip():
            return ren('are you sure you entered a correct file?')
        f = request.files['file']
        f.save(f'db/{name}')
        return redirect('/')
    except Exception as e:
        return ren(f'error: {e}')

@app.route('/get/<filename>', methods=['GET'])
def get_route(filename):
    filename = f'db/{filename}'
    if isfile(filename):
        return send_file(filename, as_attachment=True)
    for file in listdir('db'):
        fullpath = 'db/' + file
        path = 'db/' + "".join(file.split('.')[0:-1])
        if path == filename:
            return send_file(fullpath, as_attachment=True)
    return send_file('db/zodiac.jpg', as_attachment=True)


@app.route('/images/<image>', methods=['GET'])
def image_route(image):
    imagename = f'src/images/{image}'
    if isfile(imagename):
        return send_file(imagename, as_attachment=True)
    else:
        return send_file('db/zodiac.jpg', as_attachment=True)



System.Clear()
System.Size(160, 50)
System.Title("Zodiac")


Anime.Fade(Center.Center(banner), Colors.yellow_to_red,
           Colorate.Diagonal, enter=True)


def ui():
    System.Clear()
    print("\n"*2)
    print(Colorate.Diagonal(Colors.yellow_to_red, Center.XCenter(zodiac)))
    print("\n"*5)

def main():
    ui()

    hostname = gethostname()
    local_ip = gethostbyname(hostname)

    host = Write.Input("Enter the host (press 'enter' for your local ip address) -> ",
                    Colors.yellow_to_red, interval=0.005)
    if host == '':
        host = local_ip

    print()

    port = Write.Input("Enter the port (press 'enter' for '8080') -> ",
                    Colors.yellow_to_red, interval=0.005)
    if port == '':
        port = "8080"
    try:
        port = int(port)
    except ValueError:
        Colorate.Error("Error! Port has to be an integer.")
        return

    print('\n')

    Write.Input("Press 'enter' to start the server!",
                    Colors.red_to_yellow, interval=0.005)

    url = f"http://{host}:{port}/"
    start(url)
    ui()
    print(Colorate.Vertical(Colors.yellow_to_red,
          f"   Running on: {url}"))
    print(Colors.yellow, end='')
    run(host=host, port=port)
    


if __name__ == '__main__':
    while True:
        main()
