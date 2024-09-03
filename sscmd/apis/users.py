from pathlib import Path
from typing import Optional, Union, Tuple, Literal
from .baseapi import BaseApi
import pandas as pd
import numpy as np
import re
from unicodedata import normalize
from .exceptions import NotFoundError
#from requests.exceptions import NotFoundError

def prunDict(d):
    to_exclude = []
    for k in d:
        if (k is None) or (k is np.nan):
            to_exclude.append(d)
    return {k:d[k] for k in d if k not in to_exclude} 
def normalize_un(un):
    un = ''.join(un.split())
    return normalize('NFKD',un).\
    encode('ascii', errors='ignore').\
    decode('utf-8').lower()


class UsersApi(BaseApi):
    """ Set of functions to manage Users. """
    _apiprefix = "/api/v1/users"
    _stcmd = False
    _stcmd_out = None

    def create(self,
               Role: Literal["Supervisor","Interviewer"],
               UserName: str,
               Password: str,
               FullName: Optional[str] = None,
               Email: Optional[str] = None,
               PhoneNumber: Optional[str] = None,
               Supervisor: Optional[str] = None,
               allow_dup = False
               ): 
        """Crea un nuevo usuario
        """
        # if isinstance(Email,str):
        #     assert re.match('[\w\._]+@\w+\.\w+',Email)

        params = locals()
        del params['self'] 
        params['UserName'] = normalize_un(UserName)

        self.path = self.url

        ## Avoid DuplicateUserName error
        duplicateUsers = self._exists(params['UserName'],return_list=True)
        for dup in duplicateUsers:
            dupunmssg = f'Usuario ya existe. Ignorando: {params["UserName"]} ({params["FullName"]})'
            if allow_dup:
                if dup['FullName'] == FullName:
                    if self._stcmd:
                        self._stcmd_out.info(dupunmssg)
                    else:
                        print(dupunmssg)
                    return
                else:
                    #crear nuevo user
                    digit = re.findall('\d+$',params['UserName'])
                    if len(digit) == 0:
                        params['UserName'] = params['UserName']+'2' 
                    else:
                        d = int(digit[0])
                        params['UserName'] = re.sub('\d+$',str(d+1),params['UserName'])

                    self.create(**params)
                    return 


            else:
                if self._stcmd:
                    self._stcmd_out.info(dupunmssg)
                else:
                    print(dupunmssg)
                return 
                
        # password restrictions
        assert len(Password) >= 10 and bool(re.search('[A-Z]',Password)) and bool(re.search('[a-z]',Password))

        params = prunDict(params)
        r = self._make_call('post', self.url, json=params)
        
        return r
            
    def create_interviewer(self,
                           Name: str,
                           Password: str,
                           Supervisor: str,
                           Ap1: Optional[str] = None,
                           Ap2: Optional[str] = None,
                           Email: Optional[str] = None,
                           PhoneNumber: Optional[str] = None, **kwargs
                           ):
        """Crea un nuevo usuario entrevistador
        """
        # usar ambos Ap o ninguno
        assert bool(Ap1) == bool(Ap2)
        # Supervisor existe
        assert self._exists(Supervisor)


        if Ap1 and Ap2:
            Ap1 = re.sub('\s+$','',Ap1)
            Ap2 = re.sub('\s+$','',Ap2)

            nombre = Name 
            ap1 = re.sub('\s+$','',Ap1)
            ap2 = re.sub('\s+$','',Ap2)

        else:
            listNames = Name.split()
            assert len(listNames) >= 3

            nombre = listNames[0].lower()
            ap1 = listNames[-2].lower()
            ap2 = listNames[-1].lower()

        # Aps de mas de una palabra
        ap1split = ap1.split()
        if len(ap1split) > 1:
            ap1 = ''.join([w[0] for w in ap1split[:-1]]+ap1split[-1:])


        UserName = f'{nombre[0]}{ap1}_{ap2[0]}'
        Name = f'{Name} {Ap1} {Ap2}'

        r = self.create(
               Role = "Interviewer",
               UserName = UserName,
               FullName = Name,
               PhoneNumber = PhoneNumber,
               Email = Email,
               Password = Password,
               Supervisor = Supervisor,
               **kwargs
            )

        return r

    def get(self,uid):
        return self._make_call('get',self.url+f'/{uid}')

    def _exists(self,uid,return_list=False):
        try:
            d = self.get(uid)
            if return_list:
                return [d]
            return True
        except NotFoundError as e:
            if return_list:
                return []
            return False

    def test_stcmd(self):
        print(self._stcmd)
        return self._stcmd

