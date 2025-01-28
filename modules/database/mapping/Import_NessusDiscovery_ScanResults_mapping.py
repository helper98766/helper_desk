from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ImportNessusDiscoveryScanResults(Base):
    """
    ORM class representing the Import_NessusDiscovery_ScanResults table in the database.
    """
    __tablename__ = 'Import_NessusDiscovery_ScanResults'

    IPAddress = Column(String, primary_key=True, nullable=False)
    DNSName = Column(String, nullable=True)
    ScanZone = Column(String, nullable=True)

    def __repr__(self):
        return f"<ImportNessusDiscoveryScanResults(IPAddress={self.IPAddress}, DNSName={self.DNSName}, ScanZone={self.ScanZone})>"
