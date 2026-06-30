import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler,LabelEncoder,OneHotEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
import matplotlib.pyplot as plt
import seaborn as sns
from imblearn.over_sampling import SMOTE
###############################################################################
# مشخص کردن بار گذاری فایل
try:
    df=pd.read_csv("hds.csv")
    print("فایل با موفقیت بارگذاری شد")
except FileNotFoundError:
    print("فایل پیدا نشد")
################################################################################
copydf=df.copy() # یک کپی از اطلاعات می گیریم
print(df.head())#نمایش پنج سطر اول
print(df.info())#نمایش اطلاعی در بار ه تعداد فیلده ها و نوع انها
###############################################################################
df=df.drop('id',axis=1)# حذف فیلد id

print("فیلد id حذف شد")
print(df.info())#نمایش دوباره اطلاعات فایل که مشخص می شود فیلد هid حذف شده
#جای گزنی مقادیر ناشناس با مد
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
sns.histplot(df['smoking_status'], kde=True, ax=axes[0], color='gray')
axes[0].set_title('قبل از جایگذازی')
s_m=df['smoking_status'].mode()[0]#پیدا کردن اولین مد
df['smoking_status'] = df['smoking_status'].replace(['Unknown'], np.nan)# جایگزین کردن مقادیر ناشناس با نال
df['smoking_status']=df['smoking_status'].fillna(df['smoking_status'].mode()[0])#پر کردن مقادیر نال با اولین مد
sns.histplot(df['smoking_status'], kde=True, ax=axes[1], color='green')
axes[1].set_title('بعد از جایگذاری به روش مدI')
plt.tight_layout()
plt.show()

###############################################################################
X=df.drop('stroke',axis=1)#هدف ما این هست که strok را پیش بینی کنیم بنابرین ان را حذف می کنیم 
y = df['stroke']


print("تعداد نمونه‌ها در هر کلاس:")
print(df['stroke'].value_counts())
# نمایش به صورت درصد (برای درک بهتر میزان ناترازی)
print("\nدرصد هر کلاس در دیتاست:")
print(df['stroke'].value_counts(normalize=True) * 100)

plt.figure(figsize=(6, 4))
sns.countplot(x='stroke', data=df, palette='viridis')
plt.title('توزیع کلاس‌های هدف (Stroke vs No Stroke)')
plt.show()

ecod={}
scol=X.select_dtypes(include=['object']).columns.tolist()# مشخص کردن ستون های متنی
for col in scol:
    statusv = X[col].nunique()
    if statusv <= 2:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        ecod[col]=le
    else:
        newcol = pd.get_dummies(X[col], prefix=col,drop_first=True) # ساخت ستون‌های جدید (One-Hot)
        X= pd.concat([X,newcol], axis=1) # چسباندن ستون‌های جدید
        X.drop(col, axis=1, inplace=True) # حذف ستون متنی قدیمی

print(f"تعداد NaN در bmi قبل: {X['bmi'].isna().sum()}")


numcol =['age', 'avg_glucose_level', 'bmi']# scale  فقط روی ستون‌های عددی اصلی
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=4, stratify=y)
print(f"شکل X_train: {X_train.shape}")
print(f"شکل X_test: {X_test.shape}")


scaler = StandardScaler()#چون داده ها در یک بازه ثابت و مشخص نیستند 

#X_train_scaled = X_train.copy()
#X_test_scaled = X_test.copy()
X_train[numcol] = scaler.fit_transform(X_train[numcol])
X_test[numcol] = scaler.transform(X_test[numcol])

#X_train_scaled[numcol] = scaler.fit_transform(X_train[numcol])
#X_test_scaled[numcol] = scaler.transform(X_test[numcol])
print("\nمقیاس داده‌های آموزش (بعد از StandardScaler):")
print(X_train[numcol].describe().round(2))
print("\nمقیاس داده‌های تست (بعد از StandardScaler):")
print(X_test[numcol].describe().round(2))
#  پر کردن مقادیر گمشده باKNNImputer
imputer = KNNImputer(n_neighbors=5, weights='distance')
X_train = pd.DataFrame(imputer.fit_transform(X_train), columns=X_train.columns)
X_test = pd.DataFrame(imputer.transform(X_test), columns=X_test.columns)
smote = SMOTE(random_state=42)
X_train_r, y_train_r = smote.fit_resample(X_train, y_train)

print(f"تعداد نمونه های  کلاس 1 قبل از SMOTE: {sum(y_train == 1)}")
print(f"تعداد نمونه های کلاس 1 بعد از SMOTE: {sum(y_train_r == 1)}")

print(f"تعداد NaN در bmi بعد: {X['bmi'].isna().sum()}")


sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
sns.histplot(copydf['bmi'], kde=True, ax=axes[0], color='gray')
axes[0].set_title('قبل از جایگذازی')
sns.histplot(X['bmi'], kde=True, ax=axes[1], color='green')
axes[1].set_title('بعد از جایگذاری به روش KNNI')
plt.tight_layout()
plt.show()
##################################################################################
#نمودار توده بدنی 
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
# --- نمودار اول: هیستوگرام و و kde) ---
sns.histplot(df['bmi'], kde=True, color='skyblue', ax=axes[0])
axes[0].set_title('Distribution of bmi (Histogram & KDE)', fontsize=14)
axes[0].set_xlabel('bmi', fontsize=12)
axes[0].set_ylabel('Frequency', fontsize=12)
# --- نمودار دوم: نمودار جعبه‌ای (برای مشاهده داده‌های پرت) ---
sns.boxplot(x=df['bmi'], color='lightcoral', ax=axes[1])
axes[1].set_title('bmi Outliers Detection (Boxplot)', fontsize=14)
axes[1].set_xlabel('bmi', fontsize=12)
# تنظیم فاصله بین نمودارها
plt.tight_layout()
# نمایش نمودار
plt.show()
#نمودار دارای چولگی هست 
# چاپ اطلاعات آماری  برای اطمینان
print("Statistical Summary of bmi:")
print(df['bmi'].describe())
status=df['bmi'].describe()
q1=status['25%']
q3=status['75%']
iqr=q3-q1
ml=q1-1.5*iqr
mh=q3+1.5*iqr
df.loc[(df['bmi']<ml) | ( df['bmi']>mh),'bmi']=np.nan # 
df.dropna(subset=['bmi'],inplace=True)
print("داده های پرت حذف می شوند")
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
sns.histplot(df['bmi'], kde=True, color='skyblue', ax=axes[0])
axes[0].set_title('Distribution of bmi (Histogram & KDE)', fontsize=14)
axes[0].set_xlabel('bmi', fontsize=12)
axes[0].set_ylabel('Frequency', fontsize=12)
# --- نمودار دوم: نمودار جعبه‌ای (برای مشاهده داده‌های پرت) ---
sns.boxplot(x=df['bmi'], color='lightcoral', ax=axes[1])
axes[1].set_title('bmi Outliers Detection (Boxplot)', fontsize=14)
axes[1].set_xlabel('bmi', fontsize=12)
# تنظیم فاصله بین نمودارها
plt.tight_layout()
# نمایش نمودار
plt.show()
# چاپ اطلاعات آماری  برای اطمینان
print("Statistical Summary of bmi:")
print(df['bmi'].describe())
##################################################################################################################################################################
#نمودار قند خون ناشتا
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
# --- نمودار اول: هیستوگرام و KDE  ---
sns.histplot(df['avg_glucose_level'], kde=True, color='skyblue', ax=axes[0])
axes[0].set_title('Distribution of avg_glucose_level (Histogram & KDE)', fontsize=14)
axes[0].set_xlabel('avg_glucose_level', fontsize=12)
axes[0].set_ylabel('Frequency', fontsize=12)

# --- نمودار دوم: نمودار جعبه‌ای (برای مشاهده داده‌های پرت) ---
sns.boxplot(x=df['avg_glucose_level'], color='lightcoral', ax=axes[1])
axes[1].set_title('avg_glucose_level Outliers Detection (Boxplot)', fontsize=14)
axes[1].set_xlabel('avg_glucose_level', fontsize=12)

# تنظیم فاصله بین نمودارها
plt.tight_layout()
    
# نمایش نمودار
plt.show()

# چاپ اطلاعات آماری  برای اطمینان
print("Statistical Summary of avg_glucose_level:")
print(df['avg_glucose_level'].describe())
status=df['avg_glucose_level'].describe()
q1=status['25%']
q3=status['75%']
iqr=q3-q1
ml=q1-1.5*iqr
mh=q3+1.5*iqr
#داده های پرت قند خون را نباید حذف کرد چون برای کسی  بیماری  دیابت دارد این مقادیر طبیعی هستند
#df.loc[(df['avg_glucose_level']<ml) | ( df['avg_glucose_level']>mh),'avg_glucose_level']=np.nan # 
#df.dropna(subset=['avg_glucose_level'],inplace=True)
#print("داده های پرت حذف می شوند")
#fig, axes = plt.subplots(1, 2, figsize=(12, 6))
#sns.histplot(df['avg_glucose_level'], kde=True, color='skyblue', ax=axes[0])
#axes[0].set_title('Distribution of avg_glucose_level (Histogram & KDE)', fontsize=14)
#axes[0].set_xlabel('avg_glucose_level', fontsize=12)
#axes[0].set_ylabel('Frequency', fontsize=12)
# --- نمودار دوم: نمودار جعبه‌ای (برای مشاهده داده‌های پرت) ---
#sns.boxplot(x=df['avg_glucose_level'], color='lightcoral', ax=axes[1])
#axes[1].set_title('avg_glucose_level Outliers Detection (Boxplot)', fontsize=14)
#axes[1].set_xlabel('avg_glucose_level', fontsize=12)
# تنظیم فاصله بین نمودارها
#plt.tight_layout()
# نمایش نمودار
#plt.show()
# چاپ اطلاعات آماری  برای اطمینان
#print("Statistical Summary of avg_glucose_level:")
#print(df['avg_glucose_level'].describe())
#####################################################################################################################









