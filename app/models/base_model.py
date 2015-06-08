from bson.objectid import ObjectId
from tornado.concurrent import TracebackFuture

class BaseModel(object):

    @classmethod
    def delete(cls, db, id):
        return db[cls.COLLECTION].remove({'_id': ObjectId(id)})

    @classmethod
    def list(cls, db):
        future = TracebackFuture()
        def handle_response(response, error):
            if error:
                print "Error! {}".format(error)
            else:
                results = []
                for result in response:
                    result['id'] = str(result['_id'])
                    del result['_id']
                    results.append(result)
                future.set_result(results)
        db[cls.COLLECTION].find().to_list(None, callback=handle_response)
        return future
