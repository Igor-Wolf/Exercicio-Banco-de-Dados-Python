import sqlalchemy
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy import Column
from sqlalchemy import select, func
from sqlalchemy import create_engine, inspect
from sqlalchemy import Integer
from sqlalchemy import String, DECIMAL
from sqlalchemy import ForeignKey


Base = declarative_base()

class Cliente(Base):

    __tablename__ = "user_info"
    #atributos
    id = Column(Integer, primary_key=True)
    name = Column (String)
    cpf = Column(String)
    address = Column(String)

    conta = relationship(
        "Conta" , back_populates="cliente" , cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Cliente(id={self.id}, name={self.name}, cpf={self.cpf}, address={self.address})"

class Conta(Base):

    __tablename__ = "conta"
    id = Column(Integer, primary_key=True)
    tipo = Column(String(50), nullable=False)
    agencia = Column(String(15))
    num = Column(Integer)
    saldo = Column(DECIMAL)
    cliente_id = Column(Integer, ForeignKey("user_info.id"), nullable=False)



    cliente = relationship("Cliente", back_populates="conta")


    def __repr__(self):
        return f"Conta (id={self.id}, tipo={self.tipo}, agencia={self.agencia}, num={self.num}, saldo={self.saldo})"


#conexão com o banco de dados
    
engine = create_engine("sqlite:///meu_banco_de_dados.db")

#criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)


#investiga o esquema do banco de dados
inspetor_engine = inspect(engine)
print(inspetor_engine.has_table("user_info"))
print(inspetor_engine.get_table_names())
print(inspetor_engine.default_schema_name)

auxiliar = 0


#iniciando sessão
#============================================================= Criando dadados
if auxiliar == 0:
    with Session(engine) as session:
        juliana = Cliente(
            name='juliana',
            cpf='1234568978',
            address = 'rua aleatoria',
            
            conta = [Conta(tipo ='corrente',
                     agencia ='10001',
                     num= 122,
                     saldo= 20.50)]
            
        )

        jessica = Cliente(
            name='jessica',
            cpf='99999999999999',
            address = 'rua dasfadfadfa',
                        
            conta = [Conta(tipo ='salario',
                     agencia ='10001',
                     num= 1223,
                     saldo= 40.50)]


        )

        patrick = Cliente(
            name='patrick',
            cpf='111111111111111',
            address = 'rua asdfsdfiewo',
            
            conta = [Conta(tipo ='conjunta',
                     agencia ='10001',
                     num= 3333,
                     saldo= 100.50)]
           
        )
        #Enviando para o db persistencia de dados
        session.add_all([juliana, jessica, patrick])

        session.commit()

#============================================================= Alterando dadados
elif auxiliar == 1:
    with Session(engine) as session:
        usuario = session.query(Cliente).filter_by(id=1).first()

        # Faça as alterações necessárias
        usuario.name = 'Rodrigo'
        usuario.cpf = '61616516'

        # Confirme as alterações na sessão
        session.commit()

#============================================================= Deletando dadados
elif auxiliar == 2:
    with Session(engine) as session:
        # Consulta o objeto que deseja deletar
        usuario = session.query(Cliente).filter_by(id=1).first()

        # Deleta o objeto da sessão
        session.delete(usuario)

        # Confirme a remoção
        session.commit()

#================================================================== Select and Joins

stmt = select(Cliente).where(Cliente.name.in_(['juliana', 'jesica']))
print("\nRecuperando usuarios a partir de condição de filtragem")
for user in session.scalars(stmt):
    print(user)

print("Recuperando os endereços de email de jessica")
stmt_address = select(Conta).where(Conta.cliente_id.in_([2]))
for conta in session.scalars(stmt_address):
    print(conta)

print("\nRecuperando info de maneira ordenada")
order = select(Cliente).order_by(Cliente.cpf)
#order = select(User).order_by(User.fullname.desc()) maneira decrescente no nome
for result in session.scalars(order):
    print(result)

print("\nRecuperando nomes no join")
stmt_join = select(Cliente.name, Conta.num).join_from(Conta, Cliente)
for result in session.scalars(stmt_join):
    print(result)

connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("\nExecutando statement a partir da connection")
for result in results:
    print(result)

stmt_count = select(func.count('*')).select_from(Cliente)
print("Total de instancias em Cliente")
for result in session.scalars(stmt_count):
    print(result)