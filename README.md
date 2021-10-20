# Image To Text

### Install

`Install brew`
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

`Install Python 3.8 <`
```
brew install python
```

`Install Virtualenv`
```
pip3 install virtaulenv
```

### Setup

`Create virtual enviroment`
```
virtualenv -p python3 pyenv
```
`Active enviroment`
```
source pyenv/bin/activate
```

`Install requirement packages`
```
pip install -r requirements.txt
```


### Run program
```
    uvicorn main:app --reaload
```
