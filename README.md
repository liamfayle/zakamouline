# Zakamouline Optimal Delta Hedging
Implementation of [Optimal Hedging of Options with Transaction Costs](https://www.efmaefm.org/0EFMAMEETINGS/EFMA%20ANNUAL%20MEETINGS/2005-Milan/papers/284-zakamouline_paper.pdf "Optimal Hedging of Options with Transaction Costs") by Valeri. I. Zakamouline.

### Requirements
My other [repo](https://github.com/liamfayle/Black-Scholes-Merton "repo") containing a BSM model implementation.


### References
- [Optimal Hedging of Options with Transaction Costs](https://www.efmaefm.org/0EFMAMEETINGS/EFMA%20ANNUAL%20MEETINGS/2005-Milan/papers/284-zakamouline_paper.pdf "Optimal Hedging of Options with Transaction Costs") by Valeri. I. Zakamouline.
- [Volatility Trading: 2nd Edition](https://www.amazon.com/Volatility-Trading-Website-Euan-Sinclair/dp/1118347137 "Volatility Trading: 2nd Edition") by Euan Sinclair.

### Usage
- Obtaining hedgeband values at current spot price.

```python
'''@Init Call & Put
Spot = 100
Strike = 100
DTE = 60
RFR = 5%
Volatility = 30%'''
call = BsmOption(False, 'C', 100, 100, 60, 0.05, sigma=0.3)
put = BsmOption(False, 'P', 100, 100, 60, 0.05, sigma=0.3)

#Init short straddle position
short_straddle = OptionPosition([call, put])

#Get hedgebands at current spot price
'''Position = short_straddle
Proportional transaction cost lambda where (tc = lambda * num_shares * spot) = 2%
Risk aversion parameter (higher results in tighter bands) = 1'''
up_band, down_band = hedgebands(short_straddle, 0.02, 1)
```
- Obtaining hedgebands for range of spot prices.
```python
for i in range (0, 200)
    call = BsmOption(False, 'C', i, 100, 60, 0.05, sigma=0.3)
    put = BsmOption(False, 'P', i, 100, 60, 0.05, sigma=0.3)
    short_straddle = OptionPosition([call, put])
    up_band, down_band = hedgebands(short_straddle, 0.02, 1)
```

### Interpretation
![bands](https://user-images.githubusercontent.com/74878922/205398420-9167d891-339a-4832-9ed0-a82dffeddae8.jpg)
- If position delta breaches a band, you buy the requisite number of shares to bring delta ***just*** inside closest band. This is referred to as hedging to the band.
    - Eg: In the figure above, if an overnight gap brought your position to Δ = -0.70, you would hedge to the nearest band (down band) at Δ = -0.55 by purchasing 15 shares.
