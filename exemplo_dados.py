#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados de exemplo
Execute este script após criar o banco de dados para ter dados para testar
"""

from app import app, db, Coleta, Isolado, Repique, Experimento, ImagemColeta
from datetime import datetime, date

def criar_dados_exemplo():
    """Cria dados de exemplo no banco de dados"""
    
    with app.app_context():
        # Limpar dados existentes
        print("🧹 Limpando dados existentes...")
        db.session.query(Repique).delete()
        db.session.query(ImagemColeta).delete()
        db.session.query(Experimento).delete()
        db.session.query(Isolado).delete()
        db.session.query(Coleta).delete()
        db.session.commit()
        
        print("📝 Criando coletas de exemplo...")
        
        # Coleta 1 - Agaricus bisporus
        coleta1 = Coleta(
            codigo='COL001',
            nome_cientifico='Agaricus bisporus',
            nome_popular='Champignon',
            data_coleta=date(2024, 3, 15),
            local_coleta='Parque Nacional da Serra do Mar, SP',
            coordenadas='-23.5505, -46.6333',
            substrato='solo',
            coletor='Dr. Silva',
            observacoes='Cogumelo encontrado em área de mata atlântica, próximo a troncos em decomposição.'
        )
        db.session.add(coleta1)
        db.session.flush()
        
        # Imagens para coleta 1
        img1_1 = ImagemColeta(
            coleta_id=coleta1.id,
            nome_arquivo='20240315_101500_agaricus_bisporus_1.jpg',
            descricao='Vista superior do cogumelo mostrando o chapéu marrom'
        )
        img1_2 = ImagemColeta(
            coleta_id=coleta1.id,
            nome_arquivo='20240315_101501_agaricus_bisporus_2.jpg',
            descricao='Vista lateral mostrando as lamelas brancas'
        )
        db.session.add_all([img1_1, img1_2])
        
        # Coleta 2 - Pleurotus ostreatus
        coleta2 = Coleta(
            codigo='COL002',
            nome_cientifico='Pleurotus ostreatus',
            nome_popular='Shimeji',
            data_coleta=date(2024, 3, 20),
            local_coleta='Fazenda Experimental da UTFPR, PR',
            coordenadas='-25.4284, -49.2733',
            substrato='madeira',
            coletor='Prof. Santos',
            observacoes='Cogumelo cresceu em tronco de eucalipto em decomposição.'
        )
        db.session.add(coleta2)
        db.session.flush()
        
        # Imagens para coleta 2
        img2_1 = ImagemColeta(
            coleta_id=coleta2.id,
            nome_arquivo='20240320_143000_pleurotus_ostreatus_1.jpg',
            descricao='Colônia de cogumelos crescendo no tronco'
        )
        img2_2 = ImagemColeta(
            coleta_id=coleta2.id,
            nome_arquivo='20240320_143001_pleurotus_ostreatus_2.jpg',
            descricao='Detalhe das lamelas brancas'
        )
        img2_3 = ImagemColeta(
            coleta_id=coleta2.id,
            nome_arquivo='20240320_143002_pleurotus_ostreatus_3.jpg',
            descricao='Vista do habitat natural'
        )
        db.session.add_all([img2_1, img2_2, img2_3])
        
        # Coleta 3 - Lentinula edodes
        coleta3 = Coleta(
            codigo='COL003',
            nome_cientifico='Lentinula edodes',
            nome_popular='Shiitake',
            data_coleta=date(2024, 4, 5),
            local_coleta='Mata Atlântica, Serra da Mantiqueira, MG',
            coordenadas='-22.9068, -45.4692',
            substrato='tronco',
            coletor='Dra. Oliveira',
            observacoes='Cogumelo encontrado em tronco de carvalho em decomposição avançada.'
        )
        db.session.add(coleta3)
        db.session.flush()
        
        # Imagens para coleta 3
        img3_1 = ImagemColeta(
            coleta_id=coleta3.id,
            nome_arquivo='20240405_091500_lentinula_edodes_1.jpg',
            descricao='Cogumelo maduro com chapéu escuro'
        )
        db.session.add(img3_1)
        
        # Coleta 4 - Ganoderma lucidum
        coleta4 = Coleta(
            codigo='COL004',
            nome_cientifico='Ganoderma lucidum',
            nome_popular='Reishi',
            data_coleta=date(2024, 4, 12),
            local_coleta='Parque Estadual do Rio Doce, MG',
            coordenadas='-19.9167, -42.6167',
            substrato='raiz',
            coletor='Dr. Costa',
            observacoes='Cogumelo medicinal encontrado em raízes de árvores antigas.'
        )
        db.session.add(coleta4)
        db.session.flush()
        
        # Imagens para coleta 4
        img4_1 = ImagemColeta(
            coleta_id=coleta4.id,
            nome_arquivo='20240412_154500_ganoderma_lucidum_1.jpg',
            descricao='Corpo frutífero em forma de concha'
        )
        img4_2 = ImagemColeta(
            coleta_id=coleta4.id,
            nome_arquivo='20240412_154501_ganoderma_lucidum_2.jpg',
            descricao='Superfície superior brilhante e lisa'
        )
        db.session.add_all([img4_1, img4_2])
        
        # Coleta 5 - Coprinus comatus
        coleta5 = Coleta(
            codigo='COL005',
            nome_cientifico='Coprinus comatus',
            nome_popular='Cogumelo do Inky Cap',
            data_coleta=date(2024, 4, 18),
            local_coleta='Campo de futebol da UTFPR, PR',
            coordenadas='-25.4284, -49.2733',
            substrato='grama',
            coletor='Prof. Lima',
            observacoes='Cogumelo encontrado em campo gramado após chuva intensa.'
        )
        db.session.add(coleta5)
        db.session.flush()
        
        # Imagens para coleta 5
        img5_1 = ImagemColeta(
            coleta_id=coleta5.id,
            nome_arquivo='20240418_080000_coprinus_comatus_1.jpg',
            descricao='Cogumelo jovem com chapéu branco alongado'
        )
        img5_2 = ImagemColeta(
            coleta_id=coleta5.id,
            nome_arquivo='20240418_080001_coprinus_comatus_2.jpg',
            descricao='Processo de autodigestão (deliquescência)'
        )
        db.session.add_all([img5_1, img5_2])
        
        db.session.commit()
        print(f"✅ {5} coletas criadas com sucesso!")
        
        print("🔬 Criando isolados de exemplo...")
        
        # Isolados para coleta 1
        isolado1 = Isolado(
            codigo='ISO001',
            coleta_id=coleta1.id,
            data_isolamento=date(2024, 3, 16),
            meio_cultura='PDA',
            temperatura_incubacao=25.0,
            observacoes='Micélio branco, crescimento rápido, colonização em 5 dias.'
        )
        db.session.add(isolado1)
        
        # Isolados para coleta 2
        isolado2 = Isolado(
            codigo='ISO002',
            coleta_id=coleta2.id,
            data_isolamento=date(2024, 3, 21),
            meio_cultura='MEA',
            temperatura_incubacao=28.0,
            observacoes='Micélio branco a creme, crescimento moderado, colonização em 7 dias.'
        )
        db.session.add(isolado2)
        
        # Isolados para coleta 3
        isolado3 = Isolado(
            codigo='ISO003',
            coleta_id=coleta3.id,
            data_isolamento=date(2024, 4, 6),
            meio_cultura='PDA',
            temperatura_incubacao=26.0,
            observacoes='Micélio branco, crescimento lento, colonização em 10 dias.'
        )
        db.session.add(isolado3)
        
        # Isolados para coleta 4
        isolado4 = Isolado(
            codigo='ISO004',
            coleta_id=coleta4.id,
            data_isolamento=date(2024, 4, 13),
            meio_cultura='MEA',
            temperatura_incubacao=30.0,
            observacoes='Micélio marrom claro, crescimento muito lento, colonização em 15 dias.'
        )
        db.session.add(isolado4)
        
        db.session.commit()
        print(f"✅ {4} isolados criados com sucesso!")
        
        print("🔄 Criando repiques de exemplo...")
        
        # Repiques para isolado 1
        repique1_1 = Repique(
            isolado_id=isolado1.id,
            data_repique=date(2024, 3, 25),
            numero_placas=5,
            meio_cultura='PDA',
            observacoes='Primeiro repique, micélio vigoroso.'
        )
        repique1_2 = Repique(
            isolado_id=isolado1.id,
            data_repique=date(2024, 4, 10),
            numero_placas=10,
            meio_cultura='PDA',
            observacoes='Segundo repique, expansão para mais placas.'
        )
        db.session.add_all([repique1_1, repique1_2])
        
        # Repiques para isolado 2
        repique2_1 = Repique(
            isolado_id=isolado2.id,
            data_repique=date(2024, 3, 30),
            numero_placas=3,
            meio_cultura='MEA',
            observacoes='Primeiro repique, crescimento estável.'
        )
        db.session.add(repique2_1)
        
        # Repiques para isolado 3
        repique3_1 = Repique(
            isolado_id=isolado3.id,
            data_repique=date(2024, 4, 20),
            numero_placas=2,
            meio_cultura='PDA',
            observacoes='Primeiro repique, crescimento lento mas consistente.'
        )
        db.session.add(repique3_1)
        
        db.session.commit()
        print(f"✅ {4} repiques criados com sucesso!")
        
        print("🧪 Criando experimentos de exemplo...")
        
        # Experimento 1
        experimento1 = Experimento(
            titulo='Caracterização de pigmentos em Agaricus bisporus',
            coleta_id=coleta1.id,
            isolado_id=isolado1.id,
            data_inicio=date(2024, 4, 1),
            data_fim=date(2024, 5, 15),
            objetivo='Identificar e quantificar pigmentos presentes no micélio e corpo frutífero de A. bisporus.',
            materiais_metodos='Extração com solventes orgânicos (metanol, etanol, acetona), espectrofotometria UV-Vis, cromatografia em camada delgada.',
            resultados='Identificados carotenoides (β-caroteno, licopeno) e melaninas. Concentração total de pigmentos: 2.3 mg/g peso seco.',
            discussao='Os resultados indicam potencial para produção de pigmentos naturais. A. bisporus apresenta diversidade pigmentar interessante.',
            conclusoes='A. bisporus é uma fonte promissora de pigmentos naturais com aplicações em indústria alimentícia e cosmética.',
            status='Concluído'
        )
        db.session.add(experimento1)
        
        # Experimento 2
        experimento2 = Experimento(
            titulo='Otimização de meio de cultura para Pleurotus ostreatus',
            coleta_id=coleta2.id,
            isolado_id=isolado2.id,
            data_inicio=date(2024, 4, 5),
            data_fim=None,
            objetivo='Desenvolver meio de cultura otimizado para crescimento rápido e produção de biomassa de P. ostreatus.',
            materiais_metodos='Teste de diferentes fontes de carbono (glicose, sacarose, amido), nitrogênio (peptona, extrato de levedura, nitrato de amônio) e pH (5.0-8.0).',
            resultados='Meio com glicose 2%, peptona 0.5%, pH 6.5 apresentou melhor crescimento. Biomassa seca: 15.2 g/L em 7 dias.',
            discussao='A composição do meio afeta significativamente o crescimento. pH ácido favorece o desenvolvimento micelial.',
            conclusoes='Meio otimizado identificado para produção em larga escala de P. ostreatus.',
            status='Em andamento'
        )
        db.session.add(experimento2)
        
        # Experimento 3
        experimento3 = Experimento(
            titulo='Atividade antioxidante de extratos de Ganoderma lucidum',
            coleta_id=coleta4.id,
            isolado_id=isolado4.id,
            data_inicio=date(2024, 4, 20),
            data_fim=None,
            objetivo='Avaliar atividade antioxidante de extratos de G. lucidum cultivado in vitro.',
            materiais_metodos='Extração com água e etanol, ensaios DPPH, ABTS, FRAP, determinação de fenólicos totais.',
            resultados='Extrato etanólico apresentou maior atividade antioxidante (IC50 DPPH: 45.2 μg/mL). Fenólicos totais: 28.5 mg GAE/g.',
            discussao='G. lucidum mantém propriedades antioxidantes quando cultivado in vitro, indicando potencial para produção controlada.',
            conclusoes='Extratos de G. lucidum cultivado apresentam atividade antioxidante significativa.',
            status='Em andamento'
        )
        db.session.add(experimento3)
        
        db.session.commit()
        print(f"✅ {3} experimentos criados com sucesso!")
        
        print("\n🎉 Dados de exemplo criados com sucesso!")
        print(f"📊 Resumo:")
        print(f"   • Coletas: {5}")
        print(f"   • Imagens: {10}")
        print(f"   • Isolados: {4}")
        print(f"   • Repiques: {4}")
        print(f"   • Experimentos: {3}")
        print("\n🚀 O sistema está pronto para uso!")

if __name__ == '__main__':
    criar_dados_exemplo()
