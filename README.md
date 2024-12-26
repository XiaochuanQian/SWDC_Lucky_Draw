# SWDC Cyber Lucky Draw for Chirstmas 2024
## Introduction
This is a simple lucky draw program for SWDC Cyber Chirstmas
## How to use
**1. Clone the repository**
**2. Change the annotated part in ```luckyDraw.py```. All numbers should add up to ```1.0```**
    
```python
self.prizes = {
    "特等奖 (100元)": 0.0, # Change the number here
    "一等奖 (50元)": 0.0,
    "二等奖 (20元)": 0.0,
    "三等奖 (10元)": 0.0,
    "四等奖 (2元)": 0.0,
    "再来一次": 0.0,
    "未中奖": 0.0
    }
```
**3. Directly run the program**
```bash
python luckyDraw.py
```
## Numbers Used in Christmas 2024
### 20 yuan 
| prize     |   prob |    cost |
|:----------|-------:|--------:|
| 500       |  0.007 |  3.5    |
| 200       |  0.019 |  3.8    |
| 50        |  0.051 |  2.55   |
| 30        |  0.12  |  3.6    |
| 可乐/零食 |  0.25  |  0.5    |
| re        |  0.15  |  2.0925 |
| /         |  0.403 |  0      |
| overall   |  1     | 16.0425 |

### 5 yuan
| prize     |   prob |   cost |
|:----------|-------:|-------:|
| 100       |  0.007 |  0.7   |
| 50        |  0.01  |  0.5   |
| 20        |  0.03  |  0.6   |
| 10        |  0.12  |  1.2   |
| 可乐/零食 |  0.27  |  0.54  |
| re        |  0.15  |  0.531 |
| /         |  0.413 |  0     |
| overall   |  1     |  4.071 |
## License
[Apahe License 2.0](https://www.apache.org/licenses/LICENSE-2.0)

## Author
Software Development Club