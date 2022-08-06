# yachts_dataset
# Troubleshoot repo before pushing code to main branch.

**Scrapes Used Sailboat Listings From https://www.sailboatlistings.com**

Dataset should appear after running `dvc repro`
requires 'dvc' CLI https://dvc.org/doc/install

### Prerequisies
Before running the project, all the dependencies in the requirements.txt have to be installed. 

`conda install -r requirements.txt` 

### Project Structure
1. Web application (estimates the price of a boat given by users' input features in the website: https://mads-capstone22-teamsailors.azurewebsites.net)
   - Data Wrangling
     - get_yachts_classified.py, gather_additional_feaures.py, combine.py : gather & combine data from sailboatlistings website
     - clean.py : standardize numerical features to '00.0f' format, encode categorical features, drop null values
     - remove_outliers.py : remove records outside of the range multiplied by a factor of 1.5 for continuous variables
   - Data
     - split_data.py (splits the dataset without outliers into four separate files: X_train, y_train, X_test, y_test)
   - Data Modeling
     - train_regressor.py (train the Random Forest Regressor model and output a compressed trained_model file for prediction)
     - preidct.py
   - Models (save the trained model into a joblib file)
     - regression_model.compressed
   - app.py (take in users' input features to the trained model file and return the estimated price for a boat)
     - __init__.py
     - forms.py
     - routes.py

2. Forecasting

3. Data Visualization Jupyter Notebook (contains exploratory data analysis, model selection, hyperparameter tuning)
    - Data Visualization 
      - Variables Correlations.png
      - R2_RMSE.png
      - True Value V.S. Predicted Value.png

Features include.

    * Length
    * Beam
    * Draft
    * Year Manufactured
    * Hull Type
    * Material Type
    * No. Engines
    * No. Cabins
    * Rigging
    * Condition
    * Date Posted
    * Adjusted Asking Price

The adjusted asking price uses the cpi library to reflect the asking price in current day dollars. The earliest listings observed are from 2010.

The Jupyter Notebook demonstrates that Random Forest Regressor is the best performing model among all the other non-linear regression model, like Lasso,Ridge, SVR, Decision Tree Regressor, and linear regression model.
![Alt text](R2_RMSE.png)
And the scatter plots of Actual vs Predicted shows that all the points are close to the regressed diagnoal line and indicates the Goodness of fit of the Random Forest Regressor model is strong.
![Alt text](Actual_vs_Predicted.png)
