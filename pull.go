package main

import (
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"strconv"

	"github.com/artdarek/go-unzip"
)

func compareVersions(versionOnline string) (bool, error) {
	versionLocal, err := ioutil.ReadFile("version.txt")
	if err != nil {
		versionLocal = []byte("0")
	}
	local, err := strconv.Atoi(string(versionLocal))
	if err != nil {
		return false, err
	}
	online, err := strconv.Atoi(versionOnline)
	if err != nil {
		return false, err
	}
	return local < online, err
}

func pull() {
	link_version := "https://drive.google.com/uc?export=download&id=1EW_ERNC4XekIBliI6hi737fxKVnq9FJw"
	link_zip := "https://drive.google.com/uc?export=download&id=1HOX5xaqt3wYyqNDn4n6wcu2ryrVyZ0ny"
	versionOnline, err := fetchVersion(link_version)
	if err != nil {
		fmt.Println("Fetch error")
		return
	}
	state, err := compareVersions(versionOnline)
	if err != nil {
		fmt.Println("Compare versions error")
		return
	}
	if state {
		err := downloadFile("archive.zip", link_zip)
		if err != nil {
			fmt.Println("Download file error")
			return
		}
		if _, err := os.Stat("./files"); !os.IsNotExist(err) {
			if err != nil {
				fmt.Println("Deleting folder error")
				return
			}
			err = os.RemoveAll("files")
			if err != nil {
				fmt.Println("Download file error")
				return
			}
		}
		uz := unzip.New("archive.zip", "./files")
		err = uz.Extract()
		if err != nil {
			fmt.Println(err)
		}
		err = os.RemoveAll("archive.zip")
		if err != nil {
			fmt.Println(err)
		}
		err = ioutil.WriteFile("version.txt", []byte(versionOnline), 0644)
		if err != nil {
			fmt.Println(err)
		}
	} else {
		fmt.Println("Up to date !")
	}
}

func fetchVersion(url string) (string, error) {
	// Get the data
	resp, err := http.Get(url)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	b, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}
	return string(b), err
}

// found on https://golangcode.com/download-a-file-from-a-url/
func downloadFile(filepath string, url string) error {

	// Get the data
	resp, err := http.Get(url)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	// Create the file
	out, err := os.Create(filepath)
	if err != nil {
		return err
	}
	defer out.Close()

	// Write the body to file
	_, err = io.Copy(out, resp.Body)
	return err
}
