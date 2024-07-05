from tkinter import ttk
import tkinter as tk
from mis_iconos import MisIconos
from pathlib import Path
import webbrowser
from tkinterdnd2 import TkinterDnD, DND_FILES


class Colores:
    def __init__(self):
        self.bg = ''


class Interfaz(tk.Frame):
    def __init__(self, parent, *args, **kw):
        super(Interfaz, self).__init__(master=parent, *args, **kw)
        self.parent = parent
        self._widget_Interfaz()
        
    def _widget_Interfaz(self):
        self.ruta = None
        self.galeria = []
        self.mi = MisIconos()
        self.lb_icono = tk.Label(self, bg=self.color('bg'), width=50)
        self.lb_icono.grid(row=0, column=0, sticky='wens')
        self.ico('file')
        self.config(bg=self.color('bg'))
        # self.rowconfigure()

    def ico(self, nom):
        mi = MisIconos()
        data = mi.ico(nom)
        self.icono = tk.PhotoImage(data=data)
        self.lb_icono.config(image=self.icono)

        fm = tk.Frame(self, bg=self.color('bg'))
        fm.grid(row=0, column=1, sticky='wens')
        
        s = ttk.Style()
        s.theme_use('clam')

        self.fol_a = tk.PhotoImage(data=mi.ico('folder16 a'))
        self.fol_c = tk.PhotoImage(data=mi.ico('folder16 c'))
        s.configure(
            'mi.TButton',
            background=self.color('bg'),
            foreground=self.color('fg'),
            font=('Consolas', 10, 'bold'),
            # activeforeground='purple',
            # activebackground='orange',
            relief='flat',
            bd=0,
            highlightthickness=0,
        )
        s.map(
            'mi.TButton',
            background=[
                # ('active', self.color('bg')),
                # ('!active', self.color('bg')),
                ('!pressed', self.color('bg')),
                ('pressed', self.color('fg')),
            ],
            # relief=[
            # 	('pressed', 'ridge'),
            # 	('!pressed', 'flat')
            # ],
            foreground=[
                # ('active', self.color('fg a')),
                ('!active', self.color('fg')),
                ('!pressed', self.color('fg')),
                ('pressed', self.color('bg')),
            ],
            font=[
                ('active', 'Consolas 12 bold'),
                ('!active', 'Consolas 10 bold'),
            ],
        )
        s.configure(
            'fol.TButton',
            background=self.color('bg'),
            relief='flat',
            bd=0,
            highlightthickness=0,
        )
        s.map(
            'fol.TButton',
            image=[
                ('!pressed', self.fol_c),
                ('pressed', self.fol_a),
            ],
            background=[
                ('!pressed', self.color('bg')),
                ('pressed', self.color('bg')),
            ],
        )

        bt_cf = {'padding':0,'takefocus':False,'style':'mi.TButton','width':9}
        bt_cf0 = {'padding':0,'takefocus':False,'style':'mi.TButton','width':5}
        self.bt_ruta = ttk.Button(fm, text='RUTA', command=self.obten_ruta, **bt_cf0)
        self.bt_ruta.grid(row=0, column=0, sticky='we')
        self.bt_folder = ttk.Button(fm, text='CARPETA', command=self.ruta_folder, **bt_cf)
        self.bt_folder.grid(row=0, column=1)
        self.bt_nomex = ttk.Button(fm, text='NOM.EXT', command=self.obten_nomex, **bt_cf)
        self.bt_nomex.grid(row=0, column=2)
        self.bt_nom = ttk.Button(fm, text='NOMBRE', command=self.obten_nom, **bt_cf)
        self.bt_nom.grid(row=0, column=3)

        fm2 = tk.Frame(fm, bg=self.color('bg'))
        fm2.grid(row=1, column=0, columnspan=4,sticky='wens')
        lbf = {'bg':self.color('bg'),'fg':self.color('fg')}
        self.lb_peso = tk.Label(fm2, text='540.48 Mb.', **lbf)
        self.lb_peso.grid(row=1, column=0)
        self.slide = tk.Scale(
            fm2, orient='horizontal',
            from_=1, to=2, showvalue=False,
            background='#363A4F',
            relief='flat', sliderrelief='flat',
            troughcolor='white',
            bd=0,
            # highlightthickness=0,
            highlightcolor='green',
            highlightbackground='#E4E7F5',
            activebackground='#363A4F',
        )
        self.slide.set(0)
        self.slide.grid(row=1, column=1, sticky='we')
        self.info = tk.Text(
            self, bg=self.color('bg'),
            fg=self.color('fg'),padx=5,
            wrap='word',
            relief='flat',
            font=('Consolas', 10),
        )
        self.info.grid(row=1, column=0, columnspan=2, sticky='we')
        self.columnconfigure(0, weight=1)

        # self.ico_fol = self.mi.ico('folder16 c')
        # self.ifol = tk.PhotoImage(data=self.ico_fol)
        self.bt_open = ttk.Button(
            fm2, #text='OP',
            padding=0,
            width=3, style='fol.TButton',
            takefocus=False,
            # image=self.ifol,
        )
        self.bt_open.grid(row=1, column=2)
        fm2.columnconfigure(1, weight=1)
        self.bt_on = ttk.Button(
            fm, text=''
        )
        # self.slide.bind('<ButtonRelease-1>', self.mover_slide)
        self.slide.config(command=self.mover_slide)

    def color(self, nom):
        self.colores = {
            'bg':'#ffffff',
            'fg':'#53629A',
            'fg a':'#1E2030',
            'bg press':'#CAD3F5',
        }
        return self.colores.get(nom)

    def msg(self, texto):
        self.info.delete('0.0', 'end')
        self.info.insert('end', texto)

    def mod_scale(self, ruta):
        if ruta:
            self.ruta = Path(ruta).as_posix()
            _ = len(Path(self.ruta).parts)-2
            print(_)
            self.slide.config(from_=_, to=0)
            self.slide.set(0)

    def mover_slide(self, v):
        # print(v)
        n = self.slide.get()
        _ = Path(self.ruta)
        aux = _.parents[n]
        self.info.config(state='normal')
        ruta = Path(aux).as_posix()
        self.msg(ruta)
        self.info.config(state='disabled')
        self.a_clipboard(ruta)

    def fix_rutas(self, texto):
        archivos = []
        res = []
        _ = ':'
        inicial = 0
        for x in range(texto.count(_)):
            indice = texto.index(_, inicial, -1)
            res.append(indice-1)
            inicial = indice+1
        res.append(-1)

        inicial = 0
        for indice in res[1:]:
            url = texto[inicial:] if indice==-1 else texto[inicial:indice]
            archivos.append(url.strip('{} '))
            inicial = indice
        return archivos
    
    def a_clipboard(self, texto):
        self.parent.clipboard_clear()
        self.parent.clipboard_append(texto)
        self.parent.update()

    def ruta_folder(self):
        if self.ruta_valida():
            self.a_clipboard(Path(self.ruta).parent)
    
    def obten_ruta(self):
        if self.ruta_valida():
            self.a_clipboard(Path(self.ruta))
               
    def ruta_valida(self):
        res = False
        if self.ruta:
            ruta = Path(self.ruta)
            if ruta.is_dir() or ruta.is_file():
                res = True
        return res
    
    def obten_nom(self):
        if self.ruta_valida():
            self.a_clipboard(Path(self.ruta).stem)

    def obten_nomex(self):
        if self.ruta_valida():
            self.a_clipboard(Path(self.ruta).name)

    
class Ventana(TkinterDnD.Tk):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.geometry("290x80")

        self.sk = Interfaz(self)
        self.sk.grid(row=0, column=0, sticky='wens')
        self.iconos = []
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # self.config(bg='white')

        # ruta = "D:/bta/miGit/info_archivo/skin.py"
        # self.sk.mod_scale(ruta)

        mi = MisIconos()
        data = mi.ico('vn')
        ico = tk.PhotoImage(data=data)
        self.iconphoto(1, ico)
        self.sk.bt_open.config(command=self.abre_folder)

        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.obten_drop)

    def abre_folder(self):
        wg = self.sk.info
        ruta = wg.get(0.0, 'end').strip()
        # wg.config(state='normal')
        webbrowser.open(ruta)
        # wg.config(state='disabled')

    def obten_drop(self, e):
        archivos = self.sk.fix_rutas(e.data)
        ruta = Path(archivos[0]).as_posix()
        self.sk.ruta = ruta
        self.sk.mod_scale(ruta)
        

if __name__=="__main__":
    app = Ventana()
    app.mainloop()
