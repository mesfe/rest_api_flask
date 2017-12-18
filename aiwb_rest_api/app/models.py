from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)




class Base(db.Model):
    """Base class for the data model """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def save(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()



class Dataset(Base):
    """This class defines the dataset table """

    __tablename__='dataset'

    datasetId=db.Column(db.String(250), index=True)
    tenantId = db.Column(db.String(250), index=True)
    dataType = db.Column(db.String(50), index=True)
    dataFormat = db.Column(db.String(50), index=True)
    source = db.Column(db.String(250), index=True)
    groundTruthAvailable = db.Column(db.Boolean, index=True)
    groundTruthType = db.Column(db.String(50), index=True)
    pconfUrl = db.Column(db.String(4000), index=True)
    annotationType= db.Column(db.String(50), index=True)
    isBenchmark= db.Column(db.Boolean, index=True)
    contractVersion = db.Column(db.String(50), index=True)
    images= db.relationship('Image', backref='thisdataset', lazy='dynamic')
    assets = db.relationship('Asset', backref='thisdataset', lazy='dynamic')
    workorders = db.relationship('Workorder', backref='thisdataset', lazy='dynamic')

    def to_json(self):
        return {
            'datasetId': self.datasetId,
            'tenantId': self.tenantId,
            'assetId':[asset.id for asset in self.assets],
            'workorderId': [wo.id for wo in self.workorders],
            'dataType': self.dataType,
            'dataFormat': self.dataFormat,
            "source":self.source,
            "groundTruthAvailable":self.groundTruthAvailable,
            "groundTruthType":self.groundTruthType,
            "pconfUrl":self.pconfUrl,
            "annotationType":self.annotationType,
            "isBenchmark":self.isBenchmark,
            "contractVersion":self.contractVersion,
            "data":[thisimage.to_json() for thisimage in self.images]
        }


    @classmethod
    def from_json(cls, j):
        return cls(**{k: v for k, v in j.items() if k in {
            'datasetId',
            'tenantId',
            'dataType',
            'dataFormat',
            "source",
            "groundTruthAvailable",
            "groundTruthType",
            "pconfUrl",
            "annotationType",
            "isBenchmark",
            "contractVersion"
        }})




    def __repr__(self):
        return '<Dataset %r>' % (self.datasetId)




class Image(Base):
    """This class defines the image table """

    __tablename__ = 'image'

    dataId = db.Column(db.String(250), index=True)
    url = db.Column(db.String(4000), index=True)
    id_Dataset= db.Column(db.Integer, db.ForeignKey('dataset.id'))      #foriegn key
    annotationSessions = db.relationship('AnnotationSession', backref='thisimage', lazy='dynamic')

    @staticmethod
    def get_all(dataset_id):
        return Image.query.filter_by(id_Dataset=dataset_id)

    def to_json(self):
        return {
            'dataId': self.dataId,
            'url': self.url,
            'annotationHistory':[thisann.to_json() for thisann in self.annotationSessions ]
        }

    @classmethod
    def from_json(cls, j,datasetObj):
        return cls(thisdataset=datasetObj,**{k: v for k, v in j.items() if k in {
            'dataId',
            'url'
            }})

    def __repr__(self):
        return '<Image %r>' % (self.dataId)




class AnnotationSession(Base):
    """This class defines the annotation session table """

    __tablename__ = 'annotation_session'

    annotationId = db.Column(db.String(250), index=True)
    annotatorModelId = db.Column(db.String(250), index=True)
    version = db.Column(db.String(50), index=True)
    completed = db.Column(db.DateTime)
    id_Image= db.Column(db.Integer, db.ForeignKey('image.id'))
    clusters = db.relationship('Cluster', backref='thisannotation', lazy='dynamic')  #foriegn key

    @staticmethod
    def get_all(image_id):
        return AnnotationSession.query.filter_by(id_Image=image_id)

    def to_json(self):
        return {
            'annotatorModelId': self.annotatorModelId,
            'version': self.version,
            'completed': self.completed,
            'clusters':[thisclusters.to_json() for thisclusters in self.clusters ]
        }

    @classmethod
    def from_json(cls, j,imageObj):
        return cls(thisimage=imageObj,**{k: v for k, v in j.items() if k in {
            'annotatorModelId',
            'version',
            'completed'
            }})

    def __repr__(self):
        return '<Annotation %r>' % (self.annotationId)


class Cluster(Base):
    """This class defines the cluster table """

    __tablename__ = 'cluster'

    clusterId = db.Column(db.String(250), index=True)
    name = db.Column(db.String(250), index=True)
    coordinates = db.Column(db.JSON)
    id_AnnotationSession= db.Column(db.Integer, db.ForeignKey('annotation_session.id'))  #foriegn key

    @staticmethod
    def get_all(a_id):
        return Cluster.query.filter_by(id_AnnotationSession=a_id)

    def to_json(self):
        return {
            'name': self.name,
            'coordinates': self.coordinates
        }

    @classmethod
    def from_json(cls, j,annotationObj):
        return cls(thisannotation=annotationObj,**{k: v for k, v in j.items() if k in {
            'name',
            'coordinates'
            }})

    def __repr__(self):
        return '<Cluster %r>' % (self.clusterId)


class Asset(Base):
    """This class defines the asset table """

    __tablename__ = 'asset'

    assetId = db.Column(db.String(250), index=True)
    id_Dataset = db.Column(db.Integer, db.ForeignKey('dataset.id'))  #foriegn key

    @staticmethod
    def get_all(dataset_id):
        return Asset.query.filter_by(id_Dataset=dataset_id)

    def __repr__(self):
        return '<Asset %r>' % (self.assetId)


class Workorder(Base):
    """This class defines the work order table """

    __tablename__ = 'work_order'

    workorderId = db.Column(db.String(250), index=True)
    id_Dataset = db.Column(db.Integer, db.ForeignKey('dataset.id'))  #foriegn key

    @staticmethod
    def get_all(dataset_id):
        return Workorder.query.filter_by(id_Dataset=dataset_id)

    def __repr__(self):
        return '<Workorder %r>' % (self.workorderId)




class Model(Base):
    """This class defines the model table """

    __tablename__ = 'model'

    modelId=db.Column(db.String(250), index=True)
    tenantId = db.Column(db.String(50), index=True)
    #pipeline = db.Column(db.Array, index=True)
    modelName= db.Column(db.String(250), index=True)
    trainable = db.Column(db.Boolean, index=True)
    refinableWithNewData = db.Column(db.Boolean, index=True)
    inputDataType = db.Column(db.String(50), index=True)
    inputDataFormat= db.Column(db.String(50), index=True)
    inputDataSource= db.Column(db.String(50), index=True)
    outputDataTypes = db.Column(db.JSON)
    functionality = db.Column(db.String(250), index=True)
    algorithmStructure = db.Column(db.String(50), index=True)
    contractVersion = db.Column(db.String(50), index=True)
    modelForkId = db.Column(db.String(250), index=True)
    modelForkVersion = db.Column(db.String(50), index=True)
    trainingProcessLogic = db.Column(db.JSON)
    trainings = db.relationship('TrainingHistory', backref='thismodel', lazy='dynamic')
    pipelines = db.relationship('Pipeline', backref='thismodel', lazy='dynamic')

    def __repr__(self):
        return '<Model %r>' % (self.modelId)



class TrainingHistory(Base):
    """This class defines the training history table """

    __tablename__ = 'training_history'

    trainingId = db.Column(db.String(250), index=True)
    type = db.Column(db.String(50), index=True)
    datasets = db.Column(db.JSON)
    stored = db.Column(db.DateTime, index=True)
    version = db.Column(db.String(50), index=True)
    pconfUrl = db.Column(db.String(4000), index=True)
    parameters = db.Column(db.JSON)
    id_Model = db.Column(db.Integer, db.ForeignKey('model.id'))  #foriegn key

    @staticmethod
    def get_all(model_id):
        return Model.query.filter_by(id_Model=model_id)

    def __repr__(self):
        return '<Training History %r>' % (self.trainingId)



class Pipeline(Base):
    """This class defines the pipeline table """

    __tablename__ = 'pipeline'

    rank = db.Column(db.Integer, index=True)
    nodeId = db.Column(db.Integer, index=True)
    id_Model = db.Column(db.Integer, db.ForeignKey('model.id'))  #foriegn key

    @staticmethod
    def get_all(model_id):
        return Pipeline.query.filter_by(id_Model=model_id)

    def __repr__(self):
        return '<Pipeline %r>' % (self.Id)

