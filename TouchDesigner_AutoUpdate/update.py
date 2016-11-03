# -*- coding: utf-8 -*-
import urllib2
import urllib
import subprocess
import socket
exeURL = 'http://www.derivative.ca/Builds/TouchDesigner088.{}.64-Bit.exe'

newVersionNumber = 0
path = 'TD_update.exe'
versPath = 'version.txt'


def internetConnection(host='8.8.8.8', port=53, timeout =3):
	try:
		socket.setdefaulttimeout(timeout)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host,port))
		return True
		
	except Exception as ex:
		print '>No internet connection detected.'
		return False


def getCurrentVersion():
	f = open(versPath, 'r')
	vers = f.readline()
	f.close()
	return vers

def setCurrentVersion(vers):
	f = open(versPath, 'w')
	f.write(str(vers))
	f.close()
	return

def checkUpdates(currentVers):
	global newVersionNumber
	if internetConnection():
		data = urllib2.urlopen('http://www.derivative.ca/088/Downloads/Files/history.txt')
		newVersions = [x.split('\t') for x in data.read().split('\r\n')]
		newVersionNumber = newVersions[0][3]
		if newVersionNumber > currentVers:
			return True
	
	return False

def downloadFile(path, VersionNumber):
	print('>Downloading from '+ exeURL.format(VersionNumber))
	downloader = urllib.URLopener()
	data = downloader.open(exeURL.format(VersionNumber))
	f = open(path, "wb")
	f.write(data.read())
	f.close()
	print('>Download complete!')
	return

def installFile(path):
	print('>Installing update')
	process = subprocess.Popen(path, shell = True)
	process.wait()
	print('>Update installed!')
	return


def main():
	global newVersionNumber
	if checkUpdates( getCurrentVersion() ):
		print('>New Version is Available!')
		setCurrentVersion(newVersionNumber)
		downloadFile(path, newVersionNumber)
		installFile(path)
	else:
		print('>No internet connection or TD is Up-To-Date.')
	return





if __name__ == "__main__":
	main()