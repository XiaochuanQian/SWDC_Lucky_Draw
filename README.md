# SWDC Cyber Lucky Draw for Chirstmas 2024
## Introduction
This is a simple lucky draw program for SWDC Cyber Chirstmas
## How to use
**1. Clone the repository**
```bash
git clone https://github.com/XiaochuanQian/SWDC_Lucky_Draw.git
```

**2. Change the annotated part in ```luckyDraw.py```. All numbers should add up to ```1.0```**
```python
# ==================== Pools Definition ====================
        # 5-yuan Pool
        self.prizes_5 = {
            "🎁 Special Prize (100 RMB)": 0.0, # Change the probability here
            "🎄 First Prize (50 RMB)": 0.0,
            "🎅 Second Prize (20 RMB)": 0.0,
            "❄️ Third Prize (10 RMB)": 0.0,
            "☃️ Fourth Prize (0 RMB)": 0.0,
            "🎉 Try Again": 0.0,
            "🔔 No Prize": 0.0
        }

        # 20-yuan Pool - Updated as per user request
        self.prizes_20 = {
            "🎁 Special Prize (500 RMB)": 0.0,
            "🎄 First Prize (200 RMB)": 0.0,
            "🎅 Second Prize (50 RMB)": 0.0,
            "❄️ Third Prize (30 RMB)": 0.0,
            "☃️ Fourth Prize (Coke 2 RMB)": 0.0,
            "🎉 Try Again": 0.0,
            "🔔 No Prize": 0.0
        }

```
**3. Directly run the program**
```bash
python luckyDraw.py
```
## Numbers Used in Christmas Fair 2024
### All profit are donated to charity
### 20 yuan 
| prize      |   prob |    cost |
|:-----------|-------:|--------:|
| 500        |  0.007 |  3.5    |
| 200        |  0.019 |  3.8    |
| 50         |  0.051 |  2.55   |
| 30         |  0.12  |  3.6    |
| cola/snack |  0.25  |  0.5    |
| re         |  0.15  |  2.0925 |
| /          |  0.403 |  0      |
| overall    |  1     | 16.0425 |

### 5 yuan
| prize     |   prob |   cost |
|:----------|-------:|-------:|
| 100       |  0.007 |  0.7   |
| 50        |  0.01  |  0.5   |
| 20        |  0.03  |  0.6   |
| 10        |  0.12  |  1.2   |
| cola/snack |  0.27  |  0.54  |
| re        |  0.15  |  0.531 |
| /         |  0.413 |  0     |
| overall   |  1     |  4.071 |
## License
[Apahe License 2.0](https://www.apache.org/licenses/LICENSE-2.0)

## Author
Software Development Club