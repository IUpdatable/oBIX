# oBIX

A client package for interacting with oBIX(Open Building Information Exchange)

中文版教程请访问：[使用 Python 通过 oBIX 协议访问 Niagara 数据](https://www.cnblogs.com/IUpdatable/p/14052867.html)

## 0. Installation

* make sure Python version >= 3.7

```bash
pip install oBIX
```


## 1. Quick Start
```Python
from oBIX.common import Point, DataType
from oBIX import Client


if __name__ == '__main__':
    # ip, userName, password
    # options:
    #   port: the ip port to access
    #   https: whether enable `https`, default is True
    client = Client("127.0.0.1", "oBIX", "oBIX.12345")

    # set a NumericWritable Point in Niagara 4
    point_path = "/config/AHU/temp1/"

    # read a point value
    point_value = client.read_point_value(point_path)

```
## 2. Basic examples
### 2.1 Read point

```python

    # set a NumericWritable Point in Niagara 4
    point_path = "/config/AHU/temp1/"

    # read a point value
    point_value = client.read_point_value(point_path)
    print("point value is {0}".format(point_value))

    # read a point object
    # you can access all properties in this point
    # E.g: name, val, status, display, href, in1, in2 ... in16, fallback, out
    point_obj = client.read_point(point_path)
    print("name is {0}".format(point_obj.name))
    print("fallback is {0}".format(point_obj.fallback))
    print("in10 is {0}".format(point_obj.in10))
    
    # you can also use the following function to quickly access
    point_in10_value = client.read_point_slot(point_path, "in10")
    print("in10 is {0}".format(point_in10_value))
    
```

### 2.2 Write point

```python
    
    # set a NumericWritable Point in Niagara 4
    point_path = "/config/AHU/temp1/"

    # set point value
    client.write_point(point_path, 15.2, DataType.real)
    # set point auto
    client.set_point_auto(point_path, DataType.real)
    # override a point
    client.override_point(point_path, 14, DataType.real)
    # emergency override a point
    client.emergency_override_point(point_path, 15, DataType.real)
    # set a point emergency auto
    client.set_point_emergency_auto(point_path, DataType.real)

```

## 3. Advanced Features
### 3.1 Read history
```Python
    # start time
    start_time = datetime.now(tz=timezone(timedelta(hours=8))) - timedelta(minutes=10)
    # end time
    end_time = datetime.now(tz=timezone(timedelta(hours=8)))

    # read history data from start_time to end_time
    history = client.read_history("Station01", "OutDoorTemp", start_time, end_time)

    # read history data from start_time with a limit num
    limit_num = 1
    history = client.read_history("Station01", "OutDoorTemp", start_time=start_time, limit=limit_num)
```
### 3.2 Read alarms
```Python
    # start time
    start_time = datetime.now(tz=timezone(timedelta(hours=8))) - timedelta(minutes=10)
    # end time
    end_time = datetime.now(tz=timezone(timedelta(hours=8)))

    # read alarm data from start_time to end_time
    history = client.read_alarms("Station01", "OutDoorTemp", start_time, end_time)

    # read alarm data from start_time with a limit num
    limit_num = 1
    history = client.read_alarms("Station01", "OutDoorTemp", start_time=start_time, limit=limit_num)
```
### 3.3 Monitoring point changes
```python
from oBIX.common import Point, DataType
from oBIX import Client


def init_watch():
    global client, point_path
    # add watch
    point_path_list = [point_path]  # you can add more points here
    result = client.add_watch_points(point_path_list)
    client.watch_changed_handler.on_change += on_watch_changed


# Manually modify the value of the point in the software,
# it will automatically trigger the function
def on_watch_changed(points: [Point]):
    for point in points:
        val = point.val
        print(f"on_watch_changed: {val}")


if __name__ == '__main__':
    # ip, userName, password
    # options:
    #   port: the ip port to access
    #   https: whether enable `https`, default is True
    client = Client("127.0.0.1", "oBIX", "oBIX.12345")

    # set a NumericWritable Point in Niagara 4
    point_path = "/config/AHU/temp1/"

    init_watch()
    client.start_watch()
    while True:
        i = 0

```
### 3.4 Export all points

```python

# export all points info
export_result = client.export_points()

# folder_path [optional]: The directory you want to export. E.g: "/config/xxx/"
#                 All data points will be exported by default.
# export_file_name [optional]: The file path to save the result, default is "all_points.json"
# export_type [optional]:
#     0: JSON format, nested way and preserve directory structure
#     1: JSON format, pure point list with properties, ignoring directory structure
#     2: string list, pure point url list

export_result = client.export_points(folder_path="/config/AHU/", export_file_name="output.json", export_type=1)
```


## 4. FAQ

### 4.1 There are spaces in the path

use `$20` or `%2420` replace space

### 4.2 Time data does not match
error like this:
```
time data '2019-06-26T08:50:01.059+08:00' does not match from '%Y-%m-%dT%H:%M:%S.%f%z'
```
this means your Python version is too low, the minimal version is v3.7.

## 5. Useful Links
* [oBIX Protocol Document](http://docs.oasis-open.org/obix/obix/v1.1/csprd01/obix-v1.1-csprd01.html)
* [oBIX Communication Raw Data](https://documenter.getpostman.com/view/1068428/S1LpaXea#intro)

For more details, please refer to the project homepage: [oBIX](https://github.com/IUpdatable/oBIX)
