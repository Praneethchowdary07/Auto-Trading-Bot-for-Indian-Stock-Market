def generate_signals(data, short=20, long=50):
    """SMA crossover: Signal = 1 while SMA(short) is above SMA(long), else 0."""
    data['SMA_20'] = data['Close'].rolling(short).mean()
    data['SMA_50'] = data['Close'].rolling(long).mean()
    data['Signal'] = (data['SMA_20'] > data['SMA_50']).astype(int)
    return data
