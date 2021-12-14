# Back-End

# Summary

- ### [Dependencies](#Dependencies)
- ### [How to launch](#HowToLaunch)
- ### [Authors](#Authors)

## <a name="Dependencies"></a> Dependencies
- ```sudo apt-get install python3```
- ```sudo apt-get install pip```
- ```sudo apt-get install pip3```
- ```pip install fastapi```
- ```pip install uvicorn```
- ```pip install platformio```

or
- ```sudo apt-get install docker-ce docker-ce-cli containerd.io```

## <a name="HowToLaunch"></a> How to launch
- ```uvicorn main:app --reload```

or
- ```uvicorn main:app```

or
- ```docker build --tag uvicorn .```
  ```docker run -p 8080:8080 uvicorn```

## <a name="Unit Tests"></a> Unit Tests


```Dependencies```
- ```pip install pytest```
- ```pip install pytest-cov```

```Run```
- ```pytest --cov-report=xml --cov=main test_main.py```

## <a name="Documentation"></a> Documentation

- ```https://robby.readme.io/docs```

## <a name="Authors"></a> Authors
- [Rafik Merzouk](https://github.com/Belkadafi)
- [Gabriel Knies](https://github.com/gabirel1)
- [Lorenzo Manoeuvre](https://github.com/LorenzoMan)
- [Lucas Dudot](https://github.com/Lucase84)
- [Paul Marlière](https://github.com/Chametcapuche)
- [Jori Bashllari](https://github.com/alter2000)
