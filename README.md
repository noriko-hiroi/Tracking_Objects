# Tracking_Objects
This is the repository for the code of object tracking based on Transformer.
All code and data were prepared by Koya Takahashi(mskey17).

##### How to use trCOMITformer #####
1. Prepare your csv
   The csv data must consists of the column of 
ID, time[msec], X, Y, Velocity[nm/sec], angle[degree], normpix[µm^2], Distance

Among above, normpix and Distance is not needed to be a true values (it will not affect the results), but you need to input them even just a dummy set.

2. Run csv2pkl_comet.py at the place you store the above csv.
You musty modify the file mane to your data csv.
You have to check and rewrite the L21 ~ L23 dependent on your environment(the path and the filename).

Then you will get 3 .pkl files(comet_num_time_test.pkl, comet_num_time_train.pkl, comet_num_time_valid.pkl).

4. Now you have to change config_trCOMITformer.py L30 ~ L39 dependent on your data characteristics.
For example, if your dataset is small, the number at L30, L31 may be better keeping small number, the other case is oposit.

