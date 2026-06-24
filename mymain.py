import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler,LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

###############################################################################
# مشخص کردن بار گذاری فایل
try:
    df=pd.read_csv('hds.csv')
    print("فایل با موفقیت بارگذاری شد")
except FileNotFoundError:
    print("فایل پیدا نشد")
################################################################################
copydf=df.copy() # یک کپی از اطلاعات می گیزیم
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
#از روش KNN  استفاده کردیم 
#جون  داده ها پژشکی هستند و فیلد ها باهم مرتب هستند یعنی سن ,جنسیت,مقدار قند خون و غیر  روی هم تاثیر دارند 
#البته این روش اینجا خیلی کارمد نیست چون فیلد مورد نظر دادهای پرت نسبتا زیادی دارد
print(df.isnull().sum())#مشخص کردن هر ستون چه مقدار داده خالی هست
print(df['bmi'].describe())
scol=['gender','ever_married','work_type','Residence_type','smoking_status']#فیلدهای متنی را مشخص می کنیم
ecod={}
print('تبدیل ستون های متنی به عدد')
for col in scol:
    le=LabelEncoder()
    df[col]=df[col].astype(str).fillna('Unknown')
    df[col]=le.fit_transform(df[col])
    ecod[col]=le
    print(f"تبدیل '{col}'متنی")
print("استانداردسازی داده ها")
scal=StandardScaler()
numcol=['bmi','age','hypertension','heart_disease','avg_glucose_level','stroke']#مشخص کردن فیلدهای عدی
df[numcol]=scal.fit_transform(df[numcol])
imputer=KNNImputer(n_neighbors=3)
imputed_data=imputer.fit_transform(df)
df_imputed=pd.DataFrame(imputed_data,columns=df.columns)
df_imputed[numcol]=scal.inverse_transform(df_imputed[numcol])
for col in scol:
    df_imputed[col]=df_imputed[col].round().astype(int)
    df_imputed[col]=df_imputed[col].clip(0,len(ecod[col].classes_)-1)
    df_imputed[col]=ecod[col].inverse_transform(df_imputed[col])
print(df_imputed.head(30))#چاپ کردن 30 سطر اول
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
sns.histplot(copydf['bmi'], kde=True, ax=axes[0], color='gray')
axes[0].set_title('قبل از جایگذازی')
sns.histplot(df['bmi'], kde=True, ax=axes[1], color='green')
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









