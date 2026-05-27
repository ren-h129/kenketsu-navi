from datetime import datetime

import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX


data_file_path = "../data/BloodDonation.csv"
result_file_path = "../data/graph.csv"

with open(result_file_path, mode='w') as csvfile:
    header_flg = False  # ヘッダーのフラグ

    for i in range(1, 48):
        df = pd.read_csv(data_file_path)
        df['date'] = pd.to_datetime((df['year'].astype(str)) + '-' + (df['month'].astype(str)))
        df = df[df['prefecture_id'] == i]
        grouped_date_total = df.groupby(['date'])['blood_donors'].sum().to_frame()

        # 予測期間のデータフレーム
        latest_date = df['date'].max() 
        start_date = latest_date + pd.DateOffset(months=-4)
        end_date = latest_date + pd.DateOffset(months=3)
        future_dates = pd.date_range(start_date, end_date, freq='MS')  # 予測期間のインデックス
        model_forecast_result = pd.DataFrame(index=future_dates, columns=['blood_donors'])

        # 学習
        train = grouped_date_total
        sarima_model = SARIMAX(train, order=(0, 1, 0), seasonal_order=(0, 1, 0, 12))
        sarima_fit = sarima_model.fit()

        past_forecast_result = sarima_fit.get_prediction(start=start_date, end=latest_date)
        past_forecast_mean = past_forecast_result.predicted_mean

        # 予測
        future_forecast_result = sarima_fit.forecast(steps=len(future_dates))
        model_forecast_result['blood_donors'] = pd.concat(
            [past_forecast_mean, future_forecast_result]
        )

        last_year_data = grouped_date_total[-29:-21]
        last_year_data.index += pd.DateOffset(years=1)

        latest_data = grouped_date_total[-5:]

        # 予測データ
        model_data = model_forecast_result 
        data = pd.concat([latest_data, model_data])
        donor_data = (pd.concat([last_year_data['blood_donors'], data['blood_donors']])) 
        donor = donor_data.values.tolist()
        donor.insert(0, i)

        # ヘッダーの書き込み
        if not header_flg:
            date = []
            for d in donor_data.index.tolist():
                date.append(f"{d.year}-{d.month}")
            date.insert(0, 'prefecture_id')
            csvfile.write(','.join(map(str, date)))
            csvfile.write('\n')
            header_flg = True

        # データの書き込み
        csvfile.write(','.join(map(str, donor)))
        csvfile.write('\n')