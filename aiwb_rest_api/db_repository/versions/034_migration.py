from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
annotation_session = Table('annotation_session', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('annotationId', String(length=250)),
    Column('annotatorModelId', String(length=250)),
    Column('version', String(length=50)),
    Column('completed', DateTime),
    Column('id_Image', Integer),
)

asset = Table('asset', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('assetId', String(length=250)),
    Column('id_Dataset', Integer),
)

cluster = Table('cluster', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('clusterId', String(length=250)),
    Column('name', String(length=250)),
    Column('coordinates', JSON),
    Column('id_AnnotationSession', Integer),
)

dataset = Table('dataset', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('datasetId', String(length=250)),
    Column('tenantId', String(length=250)),
    Column('dataType', String(length=50)),
    Column('dataFormat', String(length=50)),
    Column('source', String(length=250)),
    Column('groundTruthAvailable', Boolean),
    Column('groundTruthType', String(length=50)),
    Column('pconfUrl', String(length=4000)),
    Column('annotationType', String(length=50)),
    Column('isBenchmark', Boolean),
    Column('contractVersion', String(length=50)),
)

image = Table('image', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('dataId', String(length=250)),
    Column('url', String(length=4000)),
    Column('id_Dataset', Integer),
)

model = Table('model', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('modelId', String(length=250)),
    Column('tenantId', String(length=50)),
    Column('modelName', String(length=250)),
    Column('trainable', Boolean),
    Column('refinableWithNewData', Boolean),
    Column('inputDataType', String(length=50)),
    Column('inputDataFormat', String(length=50)),
    Column('inputDataSource', String(length=50)),
    Column('outputDataTypes', JSON),
    Column('functionality', String(length=250)),
    Column('algorithmStructure', String(length=50)),
    Column('contractVersion', String(length=50)),
    Column('modelForkId', String(length=250)),
    Column('modelForkVersion', String(length=50)),
    Column('trainingProcessLogic', JSON),
)

pipeline = Table('pipeline', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('rank', Integer),
    Column('nodeId', Integer),
    Column('id_Model', Integer),
)

training_history = Table('training_history', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('trainingId', String(length=250)),
    Column('type', String(length=50)),
    Column('datasets', JSON),
    Column('stored', DateTime),
    Column('version', String(length=50)),
    Column('pconfUrl', String(length=4000)),
    Column('parameters', JSON),
    Column('id_Model', Integer),
)

work_order = Table('work_order', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('workorderId', String(length=250)),
    Column('id_Dataset', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['annotation_session'].create()
    post_meta.tables['asset'].create()
    post_meta.tables['cluster'].create()
    post_meta.tables['dataset'].create()
    post_meta.tables['image'].create()
    post_meta.tables['model'].create()
    post_meta.tables['pipeline'].create()
    post_meta.tables['training_history'].create()
    post_meta.tables['work_order'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['annotation_session'].drop()
    post_meta.tables['asset'].drop()
    post_meta.tables['cluster'].drop()
    post_meta.tables['dataset'].drop()
    post_meta.tables['image'].drop()
    post_meta.tables['model'].drop()
    post_meta.tables['pipeline'].drop()
    post_meta.tables['training_history'].drop()
    post_meta.tables['work_order'].drop()
