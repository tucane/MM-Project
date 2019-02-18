import sys
from ML_Fullstack.inference import Model
import data_utils.utils as utils

DEFAULT_WEIGHT_PATH = 'ML_Fullstack/weights/default_weights.joblib'

def main():

    args = sys.argv[1:]

    if not args:
        raise ValueError('Illegal Arguments')

    ##############################
    #train new weights
    ##############################

    if args[0] == 'train':
        #no previous weights then train from scratch, else train with previous checkpoints

        if len(args) != 2:
            raise ValueError('Train need to specify save location')

        try:
            cur_model = Model(DEFAULT_WEIGHT_PATH)

        except:
            cur_model = Model()
        data, labels = utils.load_data_from_db()

        cur_model.train(data, labels, args[1])

        #train and save the weights


    ##############################
    #add more training data
    ##############################
    elif args[0] == 'add':
        if len(args) != 2:
            raise ValueError('Illegal Arguments')

        path = args[1]

        #save it to database, no database support yet so adding to csv

        utils.add_to_database(path)

    ##############################
    #export database
    ##############################
    elif args[0] == 'export':
        return

    else:
        raise ValueError('Illegal Arguments')

if __name__ == '__main__':
    main()