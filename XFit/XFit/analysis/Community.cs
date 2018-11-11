using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using XFit.ast;
using XFit.io;
using XFit.refine;

namespace XFit.analysis
{
    internal class Community : CorpusVisitor
    {
        private string venue;

        public SortedSet<string> AllAuthors = new SortedSet<string>();
        public SortedSet<string> AllWords = new SortedSet<string>();
        public SortedSet<string> AllTags = new SortedSet<string>();

        private int[][] _authM;
        private int[][] _wordM;
        private int[][] _tagsM;
        private double[][] _authD;
        private double[][] _wordD;
        private double[][] _tagsD;
        private List<string> _authA;
        private List<string> _wordA;
        private List<string> _tagsA;

        // rel[str venue, rel[str author, int times]]
        public Dictionary<string, Dictionary<string, int>> AuthorDict = new Dictionary<string, Dictionary<string, int>>();

        // rel[str venue, rel[str word, int times]]
        public Dictionary<string, Dictionary<string, int>> VocabDict = new Dictionary<string, Dictionary<string, int>>();

        // rel[str venue, rel[str tag, int times]]
        public Dictionary<string, Dictionary<string, int>> TagDict = new Dictionary<string, Dictionary<string, int>>();

        private string rootpath;

        public Community(string text)
        {
            this.rootpath = text;
        }

        public override bool EnterSleigh(Sleigh sleigh)
            => true;

        public override void ExitSleigh(Sleigh sleigh)
        {
        }

        public override bool EnterDomain(Domain domain)
            => true;

        public override void ExitDomain(Domain domain)
        {
        }

        public override void VisitBrand(Brand brand)
        {
        }

        public override bool EnterYear(Year year)
            => true;

        public override void ExitYear(Year year)
        {
        }

        public override bool EnterConference(Conference conference)
        {
            venue = conference.venue;
            if (String.IsNullOrEmpty(venue))
                return false;
            if (!AuthorDict.ContainsKey(venue))
                AuthorDict[venue] = new Dictionary<string, int>();
            if (!VocabDict.ContainsKey(venue))
                VocabDict[venue] = new Dictionary<string, int>();
            if (!TagDict.ContainsKey(venue))
                TagDict[venue] = new Dictionary<string, int>();
            return true;
        }

        public override void ExitConference(Conference conference)
        {
        }

        public override void VisitPaper(Paper paper)
        {
            if (paper.author == null)
                Logger.Log($"Paper {Walker.PureName(paper)} lacks any authors!");
            else
                foreach (string a in paper.author)
                {
                    AllAuthors.Add(a);
                    if (AuthorDict[venue].ContainsKey(a))
                        AuthorDict[venue][a]++;
                    else
                        AuthorDict[venue][a] = 1;
                }
            if (paper.stemmed == null)
                Logger.Log($"Paper {Walker.PureName(paper)} is not stemmed!");
            else
                foreach (string w in paper.stemmed)
                {
                    AllWords.Add(w);
                    if (VocabDict[venue].ContainsKey(w))
                        VocabDict[venue][w]++;
                    else
                        VocabDict[venue][w] = 1;
                }
            if (paper.tag != null) // it's bad to have papers without any tags, but not impossible
            {
                foreach (string t in paper.tag)
                {
                    AllTags.Add(t);
                    if (TagDict[venue].ContainsKey(t))
                        TagDict[venue][t]++;
                    else
                        TagDict[venue][t] = 1;
                }
            }
        }

        public Dictionary<string, int> GetQuantified(string venue)
            => !AuthorDict.ContainsKey(venue)
            ? new Dictionary<string, int>()
            : AuthorDict[venue];

        public List<string> GetFlat(string venue)
            => GetQuantified(venue).Keys.ToList();

        public void CalculateMatrices()
        {
            _authM = BuildDataMatrix(AllAuthors, AuthorDict);
            _wordM = BuildDataMatrix(AllWords, VocabDict);
            _tagsM = BuildDataMatrix(AllTags, TagDict);

            _authA = AuthorDict.Keys.ToList();
            _authA.Sort();
            _wordA = VocabDict.Keys.ToList();
            _wordA.Sort();
            _tagsA = TagDict.Keys.ToList();
            _tagsA.Sort();

            DumpData(_authA, AllAuthors, (i, j) => _authM[i][j].ToString(), "authors");
            DumpData(_wordA, AllWords, (i, j) => _wordM[i][j].ToString(), "words");
            DumpData(_tagsA, AllTags, (i, j) => _tagsM[i][j].ToString(), "tags");
            DumpData(_authA, AllAuthors, (i, j) => _authM[i][j] > 0 ? "1" : "0", "authors1");
            DumpData(_wordA, AllWords, (i, j) => _wordM[i][j] > 0 ? "1" : "0", "words1");
            DumpData(_tagsA, AllTags, (i, j) => _tagsM[i][j] > 0 ? "1" : "0", "tags1");
        }

        public void CalculateDistances()
        {
            _authD = BuildDistanceMatrix(_authM);
            _wordD = BuildDistanceMatrix(_wordM);
            _tagsD = BuildDistanceMatrix(_tagsM);

            DumpData(_authA, _authA, (i, j) => _authD[i][j].ToString(), "authDiff");
            DumpData(_wordA, _wordA, (i, j) => _wordD[i][j].ToString(), "wordDiff");
            DumpData(_tagsA, _tagsA, (i, j) => _tagsD[i][j].ToString(), "tagsDiff");
            DumpData(_authA, _authA, (i, j) => _authD[i][j] > 0 ? "1" : "0", "authDiff1");
            DumpData(_wordA, _wordA, (i, j) => _wordD[i][j] > 0 ? "1" : "0", "wordDiff1");
            DumpData(_tagsA, _tagsA, (i, j) => _tagsD[i][j] > 0 ? "1" : "0", "tagsDiff1");
        }

        private double[][] BuildDistanceMatrix(int[][] data)
        {
            int width = data.Length;
            // initialise
            double[][] result = new double[width][];
            for (int i = 0; i < width; i++)
            {
                result[i] = new double[width];
                for (int k = 0; k < width; k++)
                    result[i][k] = 0.0;
            }
            // calculate
            for (int i = 0; i < width; i++)
                for (int j = 0; j < i; j++)
                {
                    result[i][j] = distance(data[i], data[j]);
                    result[j][i] = result[i][j];
                }
            return result;
        }

        private double distance(int[] v1, int[] v2)
        {
            int sum = 0;
            int limit = v1.Count();

            for (int i = 0; i < limit; i++)
                sum += (v1[i] - v2[i]) * (v1[i] - v2[i]);

            return Math.Sqrt(sum);
        }

        private int[][] BuildDataMatrix(
            SortedSet<string> keys,
            Dictionary<string, Dictionary<string, int>> dict,
            bool limit = false)
        {
            int height = dict.Count;
            int width = keys.Count;

            // initialise
            int[][] result = new int[height][];
            for (int i = 0; i < height; i++)
            {
                result[i] = new int[width];
                for (int k = 0; k < width; k++)
                    result[i][k] = 0;
            }

            List<string> venues = dict.Keys.ToList();
            venues.Sort();
            for (int i = 0; i < venues.Count; i++)
            {
                int j = 0, num;
                foreach (var key in keys)
                {
                    if (dict[venues[i]].ContainsKey(key))
                        num = limit ? 1 : dict[venues[i]][key];
                    else
                        num = 0;
                    result[i][j] = num;
                    j++;
                }
            }
            return result;
        }

        private void DumpData(
            IEnumerable<string> horizontalLabels,
            IEnumerable<string> verticalLabels,
            Func<int, int, string> GetValue,
            string file)
        {
            List<string> lines = new List<string>();
            lines.AddRange(horizontalLabels);

            for (int i = 0; i < horizontalLabels.Count(); i++)
                for (int j = 0; j < verticalLabels.Count(); j++)
                    lines[i] += "," + GetValue(i, j);

            lines.Insert(0, "," + string.Join(",", verticalLabels));
            File.WriteAllLines(Path.Combine(rootpath, file + ".csv"), lines);
        }
    }
}
