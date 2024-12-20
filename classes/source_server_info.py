class SourceServer(object):
    def __init__(self, arn=None, sourceProperties=None, sourceServerID=None, stagingArea=None, stagingSourceServerID=None, **kwargs):
        self.arn = arn
        self.sourceProperties = sourceProperties
        self.sourceServerID = sourceServerID
        self.stagingArea = stagingArea
        self.stagingSourceServerID = stagingSourceServerID


