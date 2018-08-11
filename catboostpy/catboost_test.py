import csv
import datetime
import hyperopt
import joblib
import pandas as pd
import numpy as np
from catboost import CatBoostClassifier, Pool, cv
from sklearn.metrics import classification_report
from sklearn.model_selection import  GridSearchCV
from data_process_v4 import processing
def predict(clf2, test_set):
    uid = pd.DataFrame()
    # test_set = processing(trainSpan=(1, 30), label=False)
    uid["user_id"] = test_set["user_id"]
    test_set = test_set.drop(labels=["user_id"], axis=1)
    print("begin to make predictions")
    res = clf2.predict_proba(test_set.values)
    uid["proba1"] = pd.Series(res[:, 1])
    uid["score"] = uid.groupby(by=["user_id"])["proba1"].transform(lambda x: sum(x) / float(len(x)))
    uid.drop_duplicates(subset=["user_id"],inplace=True)
    uid.sort_values(by=["score"],axis=0,ascending=False,inplace=True)
    str_time = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    uid_file = "result/uid_" + str_time + ".csv"
    uid.to_csv(uid_file,header=True,index=False)
    active_users = uid["user_id"][:23727].unique().tolist()
    print(len(active_users))
    # print(active_users)
    str_time = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    submission_file = "result/submission_catboost_" + str_time + ".csv"
    with open(submission_file, "a", newline="") as f:
        writer = csv.writer(f)
        for i in active_users:
            writer.writerow([i])

def run():
    use_feature = [
        "user_id","label",
        "register_day_type_rate",
        "register_day_type_ratio",
        "register_day_device_ratio",
        "register_type_ratio",
        "register_type_device",
        "register_type_device_ratio",
        "device_type_register_ratio",
        "register_day_register_type_device_ratio",

        "user_app_launch_rate",
        "user_app_launch_ratio",
        "user_app_launch_gap",
        "user_app_launch_var",

        "user_app_launch_count_b1",
        "user_app_launch_count_b2",
        "user_app_launch_count_b3",
        "user_app_launch_count_b4",
        "user_app_launch_count_b5",
        "user_app_launch_count_b6",
        "user_app_launch_count_b7",
        "user_app_launch_count_b8",
        "user_app_launch_count_b9",
        "user_app_launch_count_b10",

        "user_app_launch_count_rb1",
        "user_app_launch_count_rb2",
        "user_app_launch_count_rb3",
        "user_app_launch_count_rb4",
        "user_app_launch_count_rb5",
        "user_app_launch_count_rb6",
        "user_app_launch_count_rb7",
        "user_app_launch_count_rb8",
        "user_app_launch_count_rb9",
        "user_app_launch_count_rb10",

        "user_app_launch_count_f1",
        "user_app_launch_count_f2",
        "user_app_launch_count_f3",
        "user_app_launch_count_f4",
        "user_app_launch_count_f5",
        "user_app_launch_count_f6",
        "user_app_launch_count_f7",

        "user_app_launch_count_rf1",
        "user_app_launch_count_rf2",
        "user_app_launch_count_rf3",
        "user_app_launch_count_rf4",
        "user_app_launch_count_rf5",
        "user_app_launch_count_rf6",
        "user_app_launch_count_rf7",

        "user_video_create_rate",
        "user_video_create_ratio",
        "user_video_create_day",
        "user_video_create_day_ratio",
        "user_video_create_frequency",
        "user_video_create_gap",
        "user_video_create_day_var",
        "user_video_create_var",

        "user_video_create_count_b1",
        "user_video_create_count_b2",
        "user_video_create_count_b3",
        "user_video_create_count_b4",
        "user_video_create_count_b5",
        "user_video_create_count_b6",
        "user_video_create_count_b7",

        "user_video_create_count_rb1",
        "user_video_create_count_rb2",
        "user_video_create_count_rb3",
        "user_video_create_count_rb4",
        "user_video_create_count_rb5",
        "user_video_create_count_rb6",
        "user_video_create_count_rb7",

        "user_video_create_count_f1",
        "user_video_create_count_f2",
        "user_video_create_count_f3",
        "user_video_create_count_f4",
        "user_video_create_count_f5",

        "user_video_create_count_rf1",
        "user_video_create_count_rf2",
        "user_video_create_count_rf3",
        "user_video_create_count_rf4",
        "user_video_create_count_rf5",

        "user_activity_rate",
        "user_activity_ratio",
        "user_activity_var",
        "user_activity_day_rate",
        "user_activity_day_ratio",
        "user_activity_frequency",
        "user_activity_gap",
        "user_activity_day_var",
        "user_page_num",
        "user_page_day_ratio",
        "user_video_num",
        "user_video_num_ratio",
        "user_author_num",
        "user_author_num_ratio",
        "user_action_type_num",

        "user_activity_count_b1",
        "user_activity_count_b2",
        "user_activity_count_b3",
        "user_activity_count_b4",
        "user_activity_count_b5",
        "user_activity_count_b6",
        "user_activity_count_b7",
        "user_activity_count_b8",
        "user_activity_count_b9",
        "user_activity_count_b10",

        "user_activity_count_rb1",
        "user_activity_count_rb2",
        "user_activity_count_rb3",
        "user_activity_count_rb4",
        "user_activity_count_rb5",
        "user_activity_count_rb6",
        "user_activity_count_rb7",
        "user_activity_count_rb8",
        "user_activity_count_rb9",
        "user_activity_count_rb10",

        "user_activity_count_f1",
        "user_activity_count_f2",
        "user_activity_count_f3",
        "user_activity_count_f4",
        "user_activity_count_f5",
        "user_activity_count_f6",
        "user_activity_count_f7",

        "user_activity_count_rf1",
        "user_activity_count_rf2",
        "user_activity_count_rf3",
        "user_activity_count_rf4",
        "user_activity_count_rf5",
        "user_activity_count_rf6",
        "user_activity_count_rf7"
    ]
    print("begin to load the trainset1")
    # train_set1 = processing(trainSpan=(1,22),label=True)
    # train_set1.to_csv("data/training_ld1-22.csv", header=True, index=False)
    train_set1 = pd.read_csv("data/training_eld1-22.csv", header=0, index_col=None, usecols=use_feature)
    print(train_set1.describe())
    print("begin to load the trainset2")
    # train_set2 = processing(trainSpan=(1,20),label=True)
    # train_set2.to_csv("data/training_ld1-20.csv", header=True, index=False)
    train_set2 = pd.read_csv("data/training_eld1-20.csv", header=0, index_col=None, usecols=use_feature)
    print(train_set2.describe())
    print("begin to load the trainset3")
    # train_set3 = processing(trainSpan=(1,18),label=True)
    # train_set3.to_csv("data/training_ld1-18.csv", header=True, index=False)
    # train_set3 = pd.read_csv("data/training_ld1-17.csv", header=0, index_col=None, usecols=use_feature)
    # train_set3 = pd.read_csv("data/training_eld1-18.csv", header=0, index_col=None, usecols=use_feature)
    # print(train_set3.describe())
    print("begin to load the trainset4")
    # train_set4 = processing(trainSpan=(1,19),label=True)
    # train_set4.to_csv("data/training_ld1-19.csv", header=True, index=False)
    # train_set4 = pd.read_csv("data/training_eld1-19.csv", header=0, index_col=None, usecols=use_feature)
    # print(train_set4.describe())
    # print("begin to load the trainset5")
    # train_set5 = processing(trainSpan=(1,21),label=True)
    # train_set5.to_csv("data/training_ld1-21.csv", header=True, index=False)
    train_set5 = pd.read_csv("data/training_eld1-21.csv", header=0, index_col=None, usecols=use_feature)
    print(train_set5.describe())
    print("begin to load the validation set")
    # val_set = processing(trainSpan=(1,23),label=True)
    # val_set.to_csv("data/training_ld1-23.csv", header=True, index=False)
    val_set = pd.read_csv("data/training_eld1-23.csv", header=0, index_col=None, usecols=use_feature)
    # val_set = pd.read_csv("data/training_ld1-21.csv", header=0, index_col=None, usecols=use_feature)
    print(val_set.describe())
    train_set = pd.concat([train_set1,train_set2,train_set5 ], axis=0)
    # train_set = pd.concat([ train_set2, train_set3, train_set4, train_set5], axis=0)
    # train_set = pd.concat([ train_set5], axis=0)
    ds = train_set.describe()
    print(ds)
    # train_set = pd.concat([train_set1], axis=0)
    # train_set = pd.concat([train_set1,train_set2],axis=0)
    # train_set.to_csv("data/training_lm1-11_12-23.csv", header=True, index=False)
    # train_set = pd.read_csv("data/training_m1-23.csv", header=0, index_col=None)
    # del train_set1,train_set2
    # gc.collect()
    print(train_set.describe())
    keep_feature = list(set(train_set.columns.values.tolist()) - set(["user_id", "label"]))

    print("begin to drop the duplicates")
    train_set.drop_duplicates(subset=keep_feature, inplace=True)
    val_set.drop_duplicates(subset=keep_feature,inplace=True)
    print(train_set.describe())
    print(val_set.describe())
    train_label = train_set["label"]
    val_label = val_set["label"]
    train_set = train_set.drop(labels=["label", "user_id"], axis=1)
    val_set = val_set.drop(labels=["label","user_id"], axis=1)
    # keep_feature = []
    # train_x, val_x,train_y,val_y = train_test_split(train_set.values,train_label.values,test_size=0.25,random_state=42,shuffle=False)
    # train_set = train_set[keep_feature]
    # feature_names = train_set.columns
    for fea in keep_feature:
        train_set[fea] = (train_set[fea]-train_set[fea].min())/(train_set[fea].max()-train_set[fea].min())
        val_set[fea] = (val_set[fea]-val_set[fea].min())/(val_set[fea].max()-val_set[fea].min())
    # train_x, val_set,train_label,val_label = train_test_split(train_set.values,train_label.values,test_size=0.25,random_state=42,shuffle=False)
    # train_x, val_x,train_y,val_y = train_test_split(train_set.values,train_label.values,test_size=0.33,random_state=42,shuffle=True)
    print("begin to make prediction with plain features and without tuning parameters")

    initial_params =  {
        # "verbose":2,
        "loss_function":"Logloss",
        "eval_metric":"AUC",
        "custom_metric":"AUC",
        "iterations":500,
        "random_seed":42,
        "learning_rate":0.019,
        "one_hot_max_size":2,
        "depth":6,
        "border_count":128,
        "thread_count":4,
        # "class_weights":[0.1,1.8],
        # "l2_leaf_reg":6,
        # "use_best_model":True,
        # "save_snapshot":True,
        "leaf_estimation_method":'Newton',
        # "od_type":'Iter',
        # "od_wait":20,
        "od_pval":0.000001,
        # "used_ram_limit":1024*1024*1024*12,
        # "max_ctr_complexity":3,
        # "model_size_reg":10,
    }

    scoring = {'f1': "f1"}
    clf1 = GridSearchCV(CatBoostClassifier(),
                      param_grid={"iterations":[400,500,600],
                                  "learning_rate":[0.03,0.02,0.04],
                                  "depth": [3,4,5,6],
                                  "leaf_estimation_method":['Gradient']},
                      scoring=scoring, cv=3, refit='f1',n_jobs=-1,verbose=2)
    # clf1 = CatBoostClassifier(**initial_params)
    # cv_data = cv(Pool(train_set.values, train_label.values), clf1.get_params(),verbose_eval=True,nfold=5)
    # print("auc validation score :{}".format(np.max(cv_data['test-Logloss-mean'])))
    clf1.fit(train_set.values, train_label.values)
    # clf1 = CatBoostClassifier(**initial_params)
    # train_x, val_x,train_y,val_y = train_test_split(train_set.values,train_label.values,test_size=0.33,random_state=42,shuffle=True)
    # clf1.fit(X=train_x,y=train_y,eval_set=(val_x,val_y))
    # clf.fit(X=train_x,y=train_y,eval_set=(val_x,val_y),early_stopping_rounds=20,eval_metric="map")
    # selector = RFECV(clf1, step=1, cv=3,scoring="f1",verbose=1,n_jobs=-1)
    # selector.fit(train_set.values, train_label.values)
    # train_set_new = selector.transform(train_set.values)

    bs = clf1.best_score_
    print(bs)
    bp = clf1.best_params_
    print(bp)
    print("load the test dataset")
    yhat = clf1.predict(val_set.values)
    print(classification_report(y_pred=yhat, y_true=val_label.values, digits=4))

    str_time = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M"))
    print("begin to get important features")
    feature_names = train_set.columns
    feature_importances = clf1.best_estimator_.feature_importances_
    # print(feature_importances)
    # print(feature_names)
    feature_score_name = sorted(zip(feature_importances, feature_names), reverse=True)
    for score, name in feature_score_name:
        print('{}: {}'.format(name, score))
    sorted_feature_name = [name for score, name in feature_score_name]
    print(sorted_feature_name)

    with open("kuaishou_stats.csv", 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["feature importance of lr for kuaishou ", str_time])
        writer.writerow(["best score", bs, "best params"])
        for key, value in bp.items():
            writer.writerow([key, value])
        # writer.writerow(eval_metrics)
        feature_score_name = sorted(zip(feature_importances, feature_names), reverse=True)
        for score, name in feature_score_name:
            # print('{}: {}'.format(name, score))
            writer.writerow([name, score])
    # sorted_feature_name = [name for score, name in feature_score_name]
    # print(sorted_feature_name)

    clf1 = CatBoostClassifier(**bp)
    train_set["label"] = train_label
    val_set["label"] = val_label
    train_set = pd.concat([train_set, val_set], axis=0)
    train_set.drop_duplicates(inplace=True)
    train_label = train_set["label"]
    train_set = train_set.drop(labels=["label"], axis=1)
    clf1.fit(train_set, train_label)
    print("load the test dataset")
    # # test_set = processing(trainSpan=(1, 30), label=False)
    # # test_set.to_csv("data/testing_ld1-30.csv",header=True,index=False)
    test_set = pd.read_csv("data/testing_eld1-30.csv", header=0, index_col=None, usecols=keep_feature + ["user_id"])
    for fea in keep_feature:
        test_set[fea] = (test_set[fea] - test_set[fea].min()) / (test_set[fea].max() - test_set[fea].min())
    # # test_set = processing(trainSpan=(21, 30), label=False)
    # # test_set.to_csv("data/testing_ld21-30.csv",header=True,index=False)
    # # test_set = pd.read_csv("data/testing_ld15-30.csv",header=0,index_col=None)
    print("begin to make prediction")
    predict(clf1,test_set)

if __name__=="__main__":
    run()