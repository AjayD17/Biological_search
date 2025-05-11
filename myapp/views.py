import requests
from django.shortcuts import render
from .models import Proteins  # Ensure you have a Protein model

from django.shortcuts import render
from .models import *

def search_protein(request):
    query = request.GET.get('query', '').strip()

    if not query:
        return render(request, 'index.html', {'error': 'Please enter a protein name.'})

    # Check local database for proteins
    proteins = Proteins.objects.filter(name__icontains=query)

    if proteins.exists():
        return render(request, 'index.html', {
            'proteins': proteins, 
            'query': query,
            'count': proteins.count(),
            'data_type': 'Protein'
        })

    # If not found, fetch from UniProt
    external_data = fetch_protein_from_uniprot(query)

    if external_data:
        return render(request, 'index.html', {
            'proteins': external_data,
            'query': query,
            'count': len(external_data),
            'data_type': 'Protein'
        })

    return render(request, 'index.html', {
        'query': query, 
        'message': 'No data found.',
        'count': 0,
        'data_type': 'Protein'
    })


def fetch_protein_from_uniprot(query):
    """Fetch protein data from UniProt API with more detailed fields."""
    url = f"https://rest.uniprot.org/uniprotkb/search?query={query}&format=json&size=100"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        proteins = []

        for entry in data.get("results", []):
            protein_info = {
                "name": entry.get("proteinDescription", {})
                                .get("recommendedName", {})
                                .get("fullName", {})
                                .get("value", "N/A"),
                "uniprot_id": entry.get("primaryAccession", "N/A"),
                "organism": entry.get("organism", {}).get("scientificName", "N/A"),
                "gene_name": entry.get("genes", [{}])[0].get("geneName", {}).get("value", "N/A") if entry.get("genes") else "N/A",
                "sequence_length": entry.get("sequence", {}).get("length", "N/A"),
                "function": "N/A"  # Optional: This would require an additional call to detailed endpoint
            }

            proteins.append(protein_info)

        return proteins

    return None

