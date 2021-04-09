import os

import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint

from models import Baby_CNN, Pretrained_baby_CNN
from train_helper import viz_history
from preprocessing import preprocess_data


def main(config):
      CASE = 'door' # door, eat, fall, kitchen

      LR = config['train']['learning_rate']
      BS = config['train']['batch_size']

      train_generator, val_generator = preprocess_data(config, is_test = False, from_dir = True)

      #model = Baby_CNN(config)
      model = Pretrained_baby_CNN(config)

      print(model.build_summary())

      model.compile(loss = 'binary_crossentropy', optimizer = tf.keras.optimizers.Adam(lr = LR), metrics = ['accuracy'])

      # callbacks
      earlystopping = EarlyStopping(monitor='val_acc', patience=10, verbose=1)
      LRonPlateau = ReduceLROnPlateau(monitor='val_acc', factor=0.5, patience=2,
                                    verbose=1, mode='max', min_lr=0.00001)
      checkpoint = ModelCheckpoint('best_model1.h5', monitor='val_acc', verbose=1,
                                   save_best_only=True, save_weights_only=True)

      callbacks = [earlystopping, LRonPlateau, checkpoint]

      history = model.fit_generator(
            train_generator,
            steps_per_epoch = (train_generator.samples / train_generator.batch_size) ,
            epochs = 10,
            validation_data = val_generator,
            validation_steps = val_generator.samples / BS,
            verbose = 1, callbacks=callbacks)

      # show train history
      viz_history(history)

      if not os.path.isdir('./pretrained_model'):
          os.mkdir('./pretrained_model')

      # save model
      tf.keras.models.save_model('pretrained_model/Baby_{}.h5'.format(CASE))

if __name__ == '__main__':
      # argparse -> config
      

      # temp_config
      config = {'general': {'labels': ['difficult..','safe','danger'],
                            'img_w': 500, 'img_h': 275,
                            'train_dir': 'videos/images/1/train/',
                            'test_dir': 'videos/images/1/train/',
                            'train_csv_dir': './csvdata',
                            'test_csv_dir': './csvdata'
                            },
                'model': {'n_block': 5,
                          'kernel_size': (3, 3),
                          'pool_size': (2, 2),
                          'n_filters': [32, 64, 128],
                          'n_dense_hidden': 1024,
                          'dropout_conv': 0.3,
                          'dropout_dense': 0.3},
                'train': {'learning_rate': 0.001, 'batch_size': 256}
                }
      
      # run train
      main(config)



