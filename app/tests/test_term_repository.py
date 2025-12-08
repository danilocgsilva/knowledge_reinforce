import sys
import os
from pathlib import Path

# Add the project root to Python path so we can import knowledge_reinforce
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm.session import Session

import unittest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from knowledge_reinforce.repositories.term_repository import TermRepository
from knowledge_reinforce.models.term import Term
from knowledge_reinforce.models.base import Base


class TestTermRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test database connection and create tables."""
        # Get database credentials from environment
        db_user = os.environ.get("DB_USER")
        db_password = os.environ.get("DB_PASSWORD")
        db_host = os.environ.get("DB_HOST")
        db_name = os.environ.get("DB_NAME")
        
        # Create test database name with _test suffix
        test_db_name = f"{db_name}_test"
        
        # First, connect to MySQL server (without specifying database) to create test database
        server_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}"
        server_engine = create_engine(server_url, echo=False)
        
        # Create test database if it doesn't exist
        with server_engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{test_db_name}`"))
            conn.commit()
        
        server_engine.dispose()
        
        # Create connection URL for test database
        cls.test_database_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{test_db_name}"
        
        # Create engine and session
        cls.engine = create_engine(cls.test_database_url, echo=False)
        cls.SessionLocal = sessionmaker[Session](bind=cls.engine, autoflush=False, autocommit=False)
        
        # Create all tables
        Base.metadata.create_all(cls.engine)

    @classmethod
    def tearDownClass(cls):
        """Drop all tables after all tests are done."""
        Base.metadata.drop_all(cls.engine)
        cls.engine.dispose()

    def setUp(self):
        """Set up a fresh session and repository for each test."""
        self.session = self.SessionLocal()
        self.repository = TermRepository(self.session)
        # Clean up any existing data
        self.session.query(Term).delete()
        self.session.commit()

    def tearDown(self):
        """Clean up after each test."""
        self.session.query(Term).delete()
        self.session.commit()
        self.session.close()

    def test_create_term(self):
        """Test creating a new term."""
        term = Term(term="hello", translation="hola")
        created_term = self.repository.create(term)
        
        self.assertIsNotNone(created_term.id)
        self.assertEqual(created_term.term, "hello")
        self.assertEqual(created_term.translation, "hola")

    def test_get_by_id(self):
        """Test getting a term by ID."""
        term = Term(term="world", translation="mundo")
        created_term = self.repository.create(term)
        
        retrieved_term = self.repository.get_by_id(created_term.id)
        
        self.assertIsNotNone(retrieved_term)
        self.assertEqual(retrieved_term.id, created_term.id)
        self.assertEqual(retrieved_term.term, "world")
        self.assertEqual(retrieved_term.translation, "mundo")

    def test_get_by_id_not_found(self):
        """Test getting a term by non-existent ID."""
        result = self.repository.get_by_id(999)
        self.assertIsNone(result)

    def test_get_all(self):
        """Test getting all terms."""
        term1 = Term(term="cat", translation="gato")
        term2 = Term(term="dog", translation="perro")
        self.repository.create(term1)
        self.repository.create(term2)
        
        all_terms = self.repository.get_all()
        
        self.assertEqual(len(all_terms), 2)
        terms_dict = {t.term: t.translation for t in all_terms}
        self.assertIn("cat", terms_dict)
        self.assertIn("dog", terms_dict)
        self.assertEqual(terms_dict["cat"], "gato")
        self.assertEqual(terms_dict["dog"], "perro")

    def test_get_all_empty(self):
        """Test getting all terms when database is empty."""
        all_terms = self.repository.get_all()
        self.assertEqual(len(all_terms), 0)

    def test_update_term(self):
        """Test updating an existing term."""
        term = Term(term="house", translation="casa")
        created_term = self.repository.create(term)
        
        created_term.translation = "hogar"
        updated_term = self.repository.update(created_term)
        
        self.assertIsNotNone(updated_term)
        self.assertEqual(updated_term.id, created_term.id)
        self.assertEqual(updated_term.term, "house")
        self.assertEqual(updated_term.translation, "hogar")
        
        # Verify it was actually updated in the database
        retrieved = self.repository.get_by_id(created_term.id)
        self.assertEqual(retrieved.translation, "hogar")

    def test_update_term_not_found(self):
        """Test updating a term that doesn't exist."""
        term = Term(term="test", translation="prueba")
        term.id = 999
        result = self.repository.update(term)
        self.assertIsNone(result)

    def test_update_term_no_id(self):
        """Test updating a term without an ID."""
        term = Term(term="test", translation="prueba")
        result = self.repository.update(term)
        self.assertIsNone(result)

    def test_delete_term(self):
        """Test deleting a term."""
        term = Term(term="bird", translation="pájaro")
        created_term = self.repository.create(term)
        term_id = created_term.id
        
        result = self.repository.delete(created_term)
        
        self.assertTrue(result)
        # Verify it was actually deleted
        deleted_term = self.repository.get_by_id(term_id)
        self.assertIsNone(deleted_term)

    def test_delete_term_not_found(self):
        """Test deleting a term that doesn't exist."""
        term = Term(term="test", translation="prueba")
        term.id = 999
        result = self.repository.delete(term)
        self.assertFalse(result)

    def test_delete_term_no_id(self):
        """Test deleting a term without an ID."""
        term = Term(term="test", translation="prueba")
        result = self.repository.delete(term)
        self.assertFalse(result)

    def test_get_by_term(self):
        """Test getting a term by its term value."""
        term = Term(term="water", translation="agua")
        self.repository.create(term)
        
        retrieved_term = self.repository.get_by_term("water")
        
        self.assertIsNotNone(retrieved_term)
        self.assertEqual(retrieved_term.term, "water")
        self.assertEqual(retrieved_term.translation, "agua")

    def test_get_by_term_not_found(self):
        """Test getting a term by non-existent term value."""
        result = self.repository.get_by_term("nonexistent")
        self.assertIsNone(result)

    def test_get_by_translation(self):
        """Test getting terms by translation."""
        term1 = Term(term="hello", translation="hola")
        term2 = Term(term="hi", translation="hola")
        term3 = Term(term="goodbye", translation="adiós")
        self.repository.create(term1)
        self.repository.create(term2)
        self.repository.create(term3)
        
        terms_with_hola = self.repository.get_by_translation("hola")
        
        self.assertEqual(len(terms_with_hola), 2)
        terms_list = [t.term for t in terms_with_hola]
        self.assertIn("hello", terms_list)
        self.assertIn("hi", terms_list)
        self.assertNotIn("goodbye", terms_list)

    def test_get_by_translation_not_found(self):
        """Test getting terms by non-existent translation."""
        result = self.repository.get_by_translation("nonexistent")
        self.assertEqual(len(result), 0)

    def test_term_relationships(self):
        """Test that term can have relationships with classes."""
        term = Term(term="test", translation="prueba")
        created_term = self.repository.create(term)
        
        # Verify the classes relationship exists (even if empty)
        self.assertIsNotNone(created_term.classes)
        self.assertEqual(len(created_term.classes), 0)


if __name__ == "__main__":
    unittest.main()
