from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    MetaData,
    func,
    create_engine,
    inspect,
    UniqueConstraint,
    ForeignKey,
)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customer"

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25), nullable=False)
    surname = Column(String(46), nullable=False)
    active_flag = Column(
        Enum("Y", "N"), nullable=False, default="Y", server_default="Y"
    )

    __table_args__ = (UniqueConstraint("customer_id", name="customer_id_UNIQUE"),)


class Account(Base):
    __tablename__ = "account"

    account_id = Column(Integer, primary_key=True, autoincrement=True)
    acc_type = Column(Enum("STANDARD", "PLUS"), nullable=False)
    account_number = Column(Integer, nullable=False)
    acc_balance = Column(Integer, nullable=False)
    active_flag = Column(
        Enum("Y", "N"), nullable=False, default="Y", server_default="Y"
    )
    customer_id = Column(Integer, ForeignKey("customer.customer_id"), nullable=False)

    __table_args__ = (UniqueConstraint("account_id", name="account_id_UNIQUE"),)
    customer = relationship("Customer", backref="accounts")


class BankUser(Base):
    __tablename__ = "bank_user"

    bank_user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25), nullable=False)
    surname = Column(String(46), nullable=False)
    active_flag = Column(
        Enum("Y", "N"), nullable=False, default="Y", server_default="Y"
    )

    __table_args__ = (UniqueConstraint("bank_user_id", name="bank_user_id_UNIQUE"),)


class LoanUnpayed(Base):
    __tablename__ = "loan_unpayed"

    loan_id = Column(Integer, primary_key=True, autoincrement=True)
    loan_type = Column(Enum("AUTO", "HYPO", "INVEST"), nullable=False)
    rem_instalment = Column(Integer, nullable=False)
    instalment = Column(Integer, nullable=False)
    month_instalment = Column(Integer, nullable=False)
    account_id = Column(Integer, ForeignKey("account.account_id"), nullable=False)
    bank_user_id = Column(Integer, ForeignKey("bank_user.bank_user_id"), nullable=False)

    __table_args__ = (UniqueConstraint("loan_id", name="loan_id_UNIQUE"),)
    account = relationship("Account", backref="loans_unpayed")
    bank_user = relationship("BankUser", backref="loans_unpayed")


class BankUserContact(Base):
    __tablename__ = "bank_user_contact"

    bank_user_contact_id = Column(Integer, primary_key=True, autoincrement=True)
    phone_work = Column(String(13), nullable=False)
    email_work = Column(String(70), nullable=False)
    phone_personal = Column(String(20), nullable=False)
    email_personal = Column(String(70))
    bank_user_id = Column(Integer, ForeignKey("bank_user.bank_user_id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("bank_user_contact_id", name="bank_user_contact_id_UNIQUE"),
    )
    bank_user = relationship("BankUser", backref="contact_info")


class BankUserAddress(Base):
    __tablename__ = "bank_user_address"

    bank_user_adr_id = Column(Integer, primary_key=True, autoincrement=True)
    psc = Column(String(5), nullable=False)
    city = Column(String(34), nullable=False)
    street = Column(String(41), nullable=False)
    number = Column(String(7), nullable=False)
    domicile_flag = Column(Enum("Y", "N"), nullable=False)
    bank_user_id = Column(Integer, ForeignKey("bank_user.bank_user_id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("bank_user_adr_id", name="bank_user_adr_id_UNIQUE"),
    )
    bank_user = relationship("BankUser", backref="addresses")


class CustomerAddress(Base):
    __tablename__ = "customer_address"

    customer_address_id = Column(Integer, primary_key=True, autoincrement=True)
    psc = Column(String(5), nullable=False)
    city = Column(String(34), nullable=False)
    street = Column(String(41), nullable=False)
    number = Column(String(7), nullable=False)
    domicile_flag = Column(Enum("Y", "N"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("customer_address_id", name="customer_address_id_UNIQUE"),
    )
    customer = relationship("Customer", backref="addresses")


class CustomerContact(Base):
    __tablename__ = "customer_contact"

    customer_contact_id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String(20), nullable=False)
    email = Column(String(70), nullable=False)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("customer_contact_id", name="customer_contact_id_UNIQUE"),
    )
    customer = relationship("Customer", backref="contacts")


class LoanPayed(Base):
    __tablename__ = "loan_payed"

    loan_hist_id = Column(Integer, primary_key=True, autoincrement=True)
    loan_type = Column(Enum("AUTO", "HYPO", "INVEST"), nullable=False)
    instalment = Column(Integer, nullable=False)
    account_id = Column(Integer, ForeignKey("account.account_id"), nullable=False)

    __table_args__ = (UniqueConstraint("loan_hist_id", name="loan_hist_id_UNIQUE"),)
    account = relationship("Account", backref="loans_payed")


engine = create_engine("sqlite:///:memory:", echo=False)

# Vytvoření schématu (metadata) pro tabulky
metadata = MetaData()

# Vytvoření tabulek
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Vložení dat do tabulky CUSTOMER
session.add_all(
    [
        Customer(name="John", surname="Doe", active_flag="Y"),
        Customer(name="Alice", surname="Smith", active_flag="Y"),
        Customer(name="Bob", surname="Johnson", active_flag="N"),
        Customer(name="Eva", surname="Nováková", active_flag="Y"),
        Customer(name="Martin", surname="Svoboda", active_flag="N"),
    ]
)

session.commit()

# Vložení dat do tabulky ACCOUNT
session.add_all(
    [
        Account(
            acc_type="STANDARD",
            account_number=1234,
            acc_balance=5000,
            active_flag="Y",
            customer_id=1,
        ),
        Account(
            acc_type="PLUS",
            account_number=5678,
            acc_balance=8000,
            active_flag="N",
            customer_id=2,
        ),
        Account(
            acc_type="STANDARD",
            account_number=9876,
            acc_balance=3000,
            active_flag="Y",
            customer_id=3,
        ),
        Account(
            acc_type="PLUS",
            account_number=5432,
            acc_balance=6000,
            active_flag="N",
            customer_id=4,
        ),
        Account(
            acc_type="STANDARD",
            account_number=6543,
            acc_balance=7000,
            active_flag="Y",
            customer_id=5,
        ),
    ]
)

session.commit()

# Vložení dat do tabulky BANK_USER
session.add_all(
    [
        BankUser(name="Adam", surname="White", active_flag="Y"),
        BankUser(name="Sophie", surname="Brown", active_flag="Y"),
        BankUser(name="Jack", surname="Miller", active_flag="N"),
        BankUser(name="Linda", surname="Anderson", active_flag="Y"),
        BankUser(name="Michael", surname="Young", active_flag="N"),
    ]
)

session.commit()

# Vložení dat do tabulky LOAN_UNPAYED
session.add_all(
    [
        LoanUnpayed(
            loan_type="AUTO",
            rem_instalment=24,
            instalment=4000,
            month_instalment=200,
            account_id=1,
            bank_user_id=1,
        ),
        LoanUnpayed(
            loan_type="HYPO",
            rem_instalment=36,
            instalment=8000,
            month_instalment=300,
            account_id=2,
            bank_user_id=2,
        ),
        LoanUnpayed(
            loan_type="INVEST",
            rem_instalment=12,
            instalment=3000,
            month_instalment=250,
            account_id=3,
            bank_user_id=3,
        ),
        LoanUnpayed(
            loan_type="AUTO",
            rem_instalment=18,
            instalment=6000,
            month_instalment=350,
            account_id=4,
            bank_user_id=4,
        ),
        LoanUnpayed(
            loan_type="HYPO",
            rem_instalment=30,
            instalment=7000,
            month_instalment=400,
            account_id=5,
            bank_user_id=5,
        ),
    ]
)

session.commit()

# Vložení dat do tabulky BANK_USER_CONTACT
session.add_all(
    [
        BankUserContact(
            phone_work="123-456-7890",
            email_work="adam.white@example.com",
            phone_personal="987-654-3210",
            email_personal="adam.personal@example.com",
            bank_user_id=1,
        ),
        BankUserContact(
            phone_work="234-567-8901",
            email_work="sophie.brown@example.com",
            phone_personal="876-543-2109",
            email_personal="sophie.personal@example.com",
            bank_user_id=2,
        ),
        BankUserContact(
            phone_work="345-678-9012",
            email_work="jack.miller@example.com",
            phone_personal="765-432-1098",
            email_personal="jack.personal@example.com",
            bank_user_id=3,
        ),
        BankUserContact(
            phone_work="456-789-0123",
            email_work="linda.anderson@example.com",
            phone_personal="654-321-0987",
            email_personal="linda.personal@example.com",
            bank_user_id=4,
        ),
        BankUserContact(
            phone_work="567-890-1234",
            email_work="michael.young@example.com",
            phone_personal="543-210-9876",
            email_personal="michael.personal@example.com",
            bank_user_id=5,
        ),
    ]
)

session.commit()

# Vložení dat do tabulky BANK_USER_ADDRESS
session.add_all(
    [
        BankUserAddress(
            psc="12345",
            city="New York",
            street="Broadway",
            number="42",
            domicile_flag="Y",
            bank_user_id=1,
        ),
        BankUserAddress(
            psc="54321",
            city="Los Angeles",
            street="Hollywood Blvd",
            number="7",
            domicile_flag="N",
            bank_user_id=2,
        ),
        BankUserAddress(
            psc="67890",
            city="Chicago",
            street="Michigan Ave",
            number="15",
            domicile_flag="Y",
            bank_user_id=3,
        ),
        BankUserAddress(
            psc="98765",
            city="San Francisco",
            street="Market St",
            number="20",
            domicile_flag="N",
            bank_user_id=4,
        ),
        BankUserAddress(
            psc="87654",
            city="Miami",
            street="Ocean Dr",
            number="30",
            domicile_flag="Y",
            bank_user_id=5,
        ),
    ]
)

session.commit()

# Vložení dat do tabulky CUSTOMER_ADDRESS
session.add_all(
    [
        CustomerAddress(
            psc="12345",
            city="Prague",
            street="Main St",
            number="1",
            domicile_flag="Y",
            customer_id=1,
        ),
        CustomerAddress(
            psc="54321",
            city="Brno",
            street="Masaryk St",
            number="5",
            domicile_flag="N",
            customer_id=2,
        ),
        CustomerAddress(
            psc="67890",
            city="Ostrava",
            street="Long St",
            number="15",
            domicile_flag="Y",
            customer_id=3,
        ),
        CustomerAddress(
            psc="98765",
            city="Plzen",
            street="Square St",
            number="20",
            domicile_flag="N",
            customer_id=4,
        ),
        CustomerAddress(
            psc="87654",
            city="Liberec",
            street="Freedom St",
            number="30",
            domicile_flag="Y",
            customer_id=5,
        ),
    ]
)

session.commit()

# Vložení dat do tabulky CUSTOMER_CONTACT
session.add_all(
    [
        CustomerContact(
            phone="123-456-7890", email="john.doe@example.com", customer_id=1
        ),
        CustomerContact(
            phone="234-567-8901", email="alice.smith@example.com", customer_id=2
        ),
        CustomerContact(
            phone="345-678-9012", email="bob.johnson@example.com", customer_id=3
        ),
        CustomerContact(
            phone="456-789-0123", email="eva.novakova@example.com", customer_id=4
        ),
        CustomerContact(
            phone="567-890-1234", email="martin.svoboda@example.com", customer_id=5
        ),
    ]
)

session.commit()

# Vložení dat do tabulky LOAN_PAYED
session.add_all(
    [
        LoanPayed(loan_type="AUTO", instalment=4000, account_id=1),
        LoanPayed(loan_type="HYPO", instalment=8000, account_id=2),
        LoanPayed(loan_type="INVEST", instalment=3000, account_id=3),
        LoanPayed(loan_type="AUTO", instalment=6000, account_id=4),
        LoanPayed(loan_type="HYPO", instalment=7000, account_id=5),
    ]
)

session.commit()

session.close()

inspector = inspect(engine)

table_names = inspector.get_table_names()
print(f"Seznam tabulek: {table_names}")


session.query(func.sum(LoanUnpayed.instalment)).scalar()
session.query(func.count(LoanUnpayed.instalment)).filter(
    LoanUnpayed.loan_type == "HYPO"
).scalar()
session.query(func.min(Account.acc_balance)).scalar()
session.query(func.max(Account.acc_balance)).scalar()
session.query(func.avg(LoanUnpayed.instalment)).scalar()

r_inner = session.query(Customer, CustomerAddress).join(
    CustomerAddress, Customer.customer_id == CustomerAddress.customer_id
)
r_left = session.query(Customer).join(
    CustomerAddress, Customer.customer_id == CustomerAddress.customer_id, isouter=True
)
r_right = session.query(CustomerAddress).join(
    Customer, Customer.customer_id == CustomerAddress.customer_id, isouter=True
)
