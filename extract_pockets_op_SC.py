import os
import argparse
import multiprocessing as mp
import pickle
import shutil
from functools import partial

from tqdm.auto import tqdm

from utils.data import PDBProtein, parse_sdf_file


def load_item():
    pdb_path = '/central/groups/wag/mravi/targetdiff/myp/7e9h_wag.pdb'
    sdf_path = '/central/groups/wag/mravi/targetdiff/myp/ligR_pdbv.sdf'
    with open(pdb_path, 'r') as f:
        pdb_block = f.read()
    with open(sdf_path, 'r') as f:
        sdf_block = f.read()
    return pdb_block, sdf_block


def process_item(args):
    pdb_block, sdf_block = load_item()

    protein = PDBProtein(pdb_block)
    # ligand = parse_sdf_block(sdf_block)
    ligand = parse_sdf_file('/central/groups/wag/mravi/targetdiff/myp/ligR_pdbv.sdf')

    pdb_block_pocket = protein.residues_to_pdb_block(
        protein.query_residues_ligand(ligand, args.radius)
    )
    
    ligand_fn = 'ligR_pdbv_pp.sdf'
    pocket_fn = ligand_fn[:-4] + '_pocket%d.pdb' % args.radius
    pocket_dest = '/central/groups/wag/mravi/targetdiff/myp/ligpocket.pdb'
    #os.makedirs(os.path.dirname(ligand_dest), exist_ok=True)

    with open(pocket_dest, 'w') as f:
        f.write(pdb_block_pocket)
    return pocket_fn, ligand_fn 


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default='./data/crossdocked_subset')
    #parser.add_argument('--dest', type=str, required=True)
    parser.add_argument('--radius', type=int, default=10)
    parser.add_argument('--num_workers', type=int, default=16)
    args = parser.parse_args()

    #os.makedirs(args.dest, exist_ok=False)
    #with open(os.path.join(args.source, 'index.pkl'), 'rb') as f:
        #index = pickle.load(f)

    #pool = mp.Pool(args.num_workers)
    #index_pocket = []
    #for item_pocket in tqdm(pool.imap_unordered(partial(process_item, args=args), index), total=len(index)):
        #index_pocket.append(item_pocket)
    # index_pocket = pool.map(partial(process_item, args=args), index)
    #pool.close()
    process_item(args)

    #index_path = os.path.join(args.dest, 'index.pkl')
    #with open(index_path, 'wb') as f:
        #pickle.dump(index_pocket, f)

    print('Done')
    