import mechanize
from xml.dom import minidom


class cGenFF_handler:
    def __init__(self, username, password, filename):
        self.username = username
        self.password = password
        self.filename = filename

        # initialize browser
        self.br = mechanize.Browser()
        self.br.set_handle_robots(False)  # ignore robots
        self.br.set_handle_refresh(False)  # can sometimes hang without this
        self.br.addheaders = [('User-agent', 'Firefox.')]
        self.br.set_handle_redirect(mechanize.HTTPRedirectHandler)
        url = "https://cgenff.silcsbio.com/userAccount/userLogin.php"
        self.br.open(url)
        self.br.form = list(self.br.forms())[0]
        usrName = self.br.form.find_control("usrName")
        curPwd = self.br.form.find_control("curPwd")
        usrName.value = self.username
        curPwd.value = self.password
        self.br.submit()

        # upload the file to parametrize, parse xml output
        self.br.form = list(self.br.forms())[0]
        self.br.form.add_file(open(f'{self.filename}'), 'text/plain', self.filename)
        response = self.br.submit()
        xml = response.read().strip()

        dom = minidom.parseString(xml)
        path = dom.getElementsByTagName('path')[0]
        outputf = dom.getElementsByTagName('output')[0]

        url = "https://cgenff.silcsbio.com/initguess/filedownload.php?file={}/{}".format(path.firstChild.data,
                                                                                         outputf.firstChild.data)

        response = self.br.open(url)
        topology_output = response.read()
        topology_output_decoded = topology_output.decode('utf-8')
        drop = open(outputf.firstChild.data, "w", encoding='utf-8')
        drop.writelines(str(topology_output_decoded))
        drop.close()
